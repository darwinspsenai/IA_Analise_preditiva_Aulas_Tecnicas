"""Análises exploratórias do caso Airbnb do Rio de Janeiro (aula de pipelines).

Perguntas do roteiro (inspiradas no artigo de referência de análise exploratória do Airbnb):
  1. Qual é a localidade mais cara e a mais barata?                   -> linha
  2. Quais são os 10 bairros com média de aluguel mais baixa?          -> linha e pizza
  3. Quais são os 10 bairros com média de aluguel mais alta?           -> linha e pizza
  4. Qual é a média do número mínimo de noites para alugar um imóvel?  -> resumo e histograma
  5. Em quais dias da semana as pessoas mais ficam hospedadas?         -> linha (calendário)
  6. Como os preços se distribuem no mapa?                             -> mapa de calor sobre o mapa do Rio
  7. Como preço, hóspedes, quartos e avaliações se relacionam?         -> matriz de dispersão

Localidade = bairro (neighbourhood_cleansed): no Rio, neighbourhood_group_cleansed vem vazia.
Dias = noites reservadas no calendário (available = 'f') dos próximos 12 meses, por dia da semana.
"""
import json

import numpy as np
import pandas as pd

from pipeline_limpeza.config import DADOS_REFERENCIA
from pipeline_limpeza.graficos import Graficos
from pipeline_limpeza.visualizacao import Visualizacao

ORDEM_DIAS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
NOMES_TIPOS = {"Entire home/apt": "Casa ou apto inteiro", "Private room": "Quarto privado",
               "Shared room": "Quarto compartilhado", "Hotel room": "Quarto de hotel"}
CORES_TIPOS = {"Entire home/apt": "#2A7F87", "Private room": "#8FC1C6",
               "Shared room": "#B5523B", "Hotel room": "#5B6B72"}
VARIAVEIS_MATRIZ = ["price", "accommodates", "bedrooms", "minimum_nights",
                    "number_of_reviews", "review_scores_rating"]


class AnalisesAirbnb(Graficos):
    """Perguntas sobre a base limpa. Herda o diagnóstico (Analise) e os gráficos (Graficos)."""

    COLUNA_LOCALIDADE = "neighbourhood_cleansed"
    ARQUIVO_BAIRROS = DADOS_REFERENCIA / "bairros_rio.geojson"

    def __init__(self, dados, nome="airbnb_rio", minimo_imoveis=10):
        super().__init__(dados, nome)
        self.minimo_imoveis = minimo_imoveis

    # ------------------------------------------------------------ preços por localidade
    def precos_por_localidade(self):
        """Quantidade de imóveis, média e mediana do preço por bairro (só bairros com imóveis suficientes)."""
        tabela = (self.dados.groupby(self.COLUNA_LOCALIDADE)["price"]
                  .agg(imoveis="count", media="mean", mediana="median")
                  .round(2))
        minimo = self.minimo_imoveis
        return tabela.loc[tabela["imoveis"] >= minimo].sort_values("media", ascending=False)

    def localidades_extremas(self):
        """Devolve (bairro mais caro, bairro mais barato, tabela completa)."""
        tabela = self.precos_por_localidade()
        return tabela.index[0], tabela.index[-1], tabela

    def top_bairros(self, n=10, mais_caros=True):
        tabela = self.precos_por_localidade()
        return tabela.sort_values("media", ascending=not mais_caros)["media"].head(n)

    def linha_localidades(self):
        """Pergunta 1: a média de cada bairro, do mais barato ao mais caro, em uma linha."""
        tabela = self.precos_por_localidade().sort_values("media").reset_index()
        Visualizacao.linhas(tabela, x=self.COLUNA_LOCALIDADE, y="media",
                            titulo=f"Preço médio por bairro, do mais barato ao mais caro (com {self.minimo_imoveis}+ imóveis)",
                            rotulo_x="Bairro", rotulo_y="Preço médio (R$)", tamanho=(10, 5))

    def linha_top_bairros(self, n=10, mais_caros=True):
        """Perguntas 2 e 3: os n bairros da lista, em linha."""
        tabela = self.top_bairros(n, mais_caros).reset_index()
        if mais_caros:
            titulo = f"Os {n} bairros com maior preço médio (R$)"
        else:
            titulo = f"Os {n} bairros com menor preço médio (R$)"
        Visualizacao.linhas(tabela, x=self.COLUNA_LOCALIDADE, y="media", titulo=titulo,
                            rotulo_x="Bairro", rotulo_y="Preço médio (R$)")

    def pizza_tipos_nos_bairros(self, n=10, mais_caros=True):
        """Que tipo de imóvel predomina nos bairros da lista (perguntas 2 e 3)."""
        bairros = self.top_bairros(n, mais_caros).index
        imoveis = self.dados[self.dados[self.COLUNA_LOCALIDADE].isin(bairros)]
        tabela = (imoveis["room_type"].map(lambda t: NOMES_TIPOS.get(t, t)).value_counts()
                  .rename_axis("tipo").reset_index(name="imoveis"))
        lado = "mais caros" if mais_caros else "mais baratos"
        Visualizacao.pizza(tabela, "tipo", "imoveis", f"Tipos de acomodação nos {n} bairros {lado}")

    # ------------------------------------------------------------ noites mínimas
    def media_minimo_noites(self):
        noites = pd.to_numeric(self.dados["minimum_nights"], errors="coerce")
        return {"média": round(noites.mean(), 2),
                "mediana": float(noites.median()),
                "% com até 3 noites": round((noites <= 3).mean() * 100, 1),
                "% com 30 noites ou mais": round((noites >= 30).mean() * 100, 1),
                "n": int(noites.notna().sum())}

    # ------------------------------------------------------------ dias de hospedagem
    def dias_reservados(self, calendario):
        """% de noites reservadas por dia da semana, só para os imóveis desta base."""
        cal = calendario[calendario["listing_id"].isin(self.dados["id"])].copy()
        cal["data"] = pd.to_datetime(cal["date"], errors="coerce")
        cal = cal.dropna(subset=["data"])
        cal["reservada"] = cal["available"].eq("f")
        cal["dia_semana"] = cal["data"].dt.dayofweek
        porcentagem = cal.groupby("dia_semana")["reservada"].mean().mul(100)
        porcentagem.index = [ORDEM_DIAS[i] for i in porcentagem.index]
        return porcentagem.reindex(ORDEM_DIAS).round(1)

    def linha_dias_reservados(self, calendario):
        tabela = self.dias_reservados(calendario).rename("reservadas").rename_axis("dia").reset_index()
        Visualizacao.linhas(tabela, x="dia", y="reservadas",
                            titulo="% de noites reservadas por dia da semana (próximos 12 meses)",
                            rotulo_x="Dia da semana", rotulo_y="% de noites reservadas")

    # ------------------------------------------------------------ mapa de calor sobre o mapa do Rio
    def _contornos_bairros(self):
        """Anéis (longitude, latitude) de todos os bairros, lidos do GeoJSON de referência."""
        with open(self.ARQUIVO_BAIRROS, encoding="utf-8") as arquivo:
            geojson = json.load(arquivo)
        aneis = []
        for feicao in geojson["features"]:
            geometria = feicao["geometry"]
            poligonos = geometria["coordinates"] if geometria["type"] == "MultiPolygon" else [geometria["coordinates"]]
            for poligono in poligonos:
                aneis.extend(np.array(anel)[:, :2] for anel in poligono)  # longitude e latitude
        return aneis

    def tabela_mapa_calor(self, faixas=40, minimo_por_celula=3):
        """Preço médio em uma grade de faixas de longitude × latitude.
        Células com menos de `minimo_por_celula` imóveis ficam vazias, para não mostrar ruído."""
        dados = self.dados.dropna(subset=["latitude", "longitude", "price"])
        bordas_x = np.linspace(dados["longitude"].min(), dados["longitude"].max(), faixas + 1)
        bordas_y = np.linspace(dados["latitude"].min(), dados["latitude"].max(), faixas + 1)
        lon = pd.cut(dados["longitude"], bordas_x, labels=False, include_lowest=True)
        lat = pd.cut(dados["latitude"], bordas_y, labels=False, include_lowest=True)
        grupos = dados.groupby([lat, lon])["price"]
        medias = grupos.mean().unstack().reindex(index=range(faixas), columns=range(faixas))
        contagem = grupos.count().unstack().reindex(index=range(faixas), columns=range(faixas))
        matriz = medias.where(contagem >= minimo_por_celula).astype(float).to_numpy()  # linhas: sul -> norte
        return matriz, bordas_x, bordas_y

    def mapa_calor_sobre_mapa(self, faixas=40, minimo_por_celula=3):
        matriz, bordas_x, bordas_y = self.tabela_mapa_calor(faixas, minimo_por_celula)
        Visualizacao.mapa_calor_no_mapa(matriz, bordas_x, bordas_y, self._contornos_bairros(),
                                        titulo="Preço médio por região sobre o mapa do Rio (R$)",
                                        rotulo_valor="Preço médio (R$)")

    # ------------------------------------------------------------ várias variáveis
    def matriz_variaveis(self):
        """Matriz de dispersão: cada par de variáveis, com a cor separando o tipo de acomodação."""
        Visualizacao.matriz_dispersao(self.dados, VARIAVEIS_MATRIZ, "room_type", CORES_TIPOS,
                                      "Preço e outras variáveis, por tipo de acomodação")
