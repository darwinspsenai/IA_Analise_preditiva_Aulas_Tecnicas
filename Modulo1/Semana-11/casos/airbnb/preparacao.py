"""Prepara a amostra didática do Airbnb (Rio de Janeiro) usada na aula de pipelines.

Fonte real: Inside Airbnb (http://insideairbnb.com/get-the-data), arquivos listings.csv.gz e calendar.csv.gz
da cidade Rio de Janeiro, snapshot 2026-09-22:
  https://data.insideairbnb.com/brazil/rj/rio-de-janeiro/2026-09-22/data/listings.csv.gz
  https://data.insideairbnb.com/brazil/rj/rio-de-janeiro/2026-09-22/data/calendar.csv.gz

O que esta classe faz:
  1. lê o arquivo completo (48 mil imóveis, 90 colunas);
  2. seleciona 25 colunas usadas na aula (nomes originais em inglês, como no portal);
  3. sorteia 3.000 imóveis (semente fixa, reprodutível);
  4. pseudonimiza os nomes dos anfitriões ("Anfitrião 001"...), pois são nomes de pessoas reais;
  5. insere, DE PROPÓSITO, alguns problemas de coleta para a prática: 60 linhas duplicadas,
     15 preços zerados, 2% de nomes em branco e 4% de nomes de anfitrião ausentes.
     Todo o resto do arquivo é dado real, sem alteração;
  6. (opcional) filtra o calendar.csv.gz para os imóveis da amostra (análise de dias reservados).

Saídas: dados/brutos/airbnb_rio_bruto.csv e dados/brutos/calendario_airbnb_rio_amostra.csv.gz

Uso (na raiz do projeto):  python -m casos.airbnb.preparacao listings.csv.gz [calendar.csv.gz]
"""
import sys

import numpy as np
import pandas as pd

from pipeline_limpeza.config import DADOS_BRUTOS

SAIDA = DADOS_BRUTOS / "airbnb_rio_bruto.csv"
SAIDA_CALENDARIO = DADOS_BRUTOS / "calendario_airbnb_rio_amostra.csv.gz"

COLUNAS = [
    "id", "name", "host_name", "neighbourhood_cleansed", "neighbourhood_group_cleansed",
    "room_type", "property_type", "latitude", "longitude", "accommodates", "bedrooms",
    "beds", "bathrooms_text", "price", "minimum_nights", "maximum_nights",
    "number_of_reviews", "last_review", "reviews_per_month", "review_scores_rating",
    "availability_365", "host_is_superhost", "host_response_rate", "host_listings_count",
    "instant_bookable",
]


class PreparadorAirbnb:
    """Gera a amostra didática (dados/airbnb_rio_bruto.csv) a partir do listings.csv.gz real."""

    def __init__(self, n_amostra=3000, semente=2026):
        self.n_amostra = n_amostra
        self.rng = np.random.default_rng(semente)

    def carregar(self, caminho):
        bruto = pd.read_csv(caminho, low_memory=False)
        faltam = [c for c in COLUNAS if c not in bruto.columns]
        if faltam:
            raise ValueError(f"Colunas ausentes no arquivo do Inside Airbnb: {faltam}")
        return bruto[COLUNAS]

    def amostrar(self, dados):
        amostra = dados.sample(self.n_amostra, random_state=self.rng.integers(1_000_000)).copy()
        return amostra.reset_index(drop=True)

    def pseudonimizar(self, amostra):
        # Nomes reais viram "Anfitrião 001", na ordem em que aparecem (não é possível voltar ao nome)
        nomes = amostra["host_name"].dropna().unique()
        mapa = {nome: f"Anfitrião {i:03d}" for i, nome in enumerate(nomes, start=1)}
        amostra["host_name"] = amostra["host_name"].map(mapa)
        return amostra

    def injetar_problemas(self, amostra):
        n = len(amostra)
        # 15 preços zerados (erro de digitação ou de coleta)
        zeros = self.rng.choice(n, 15, replace=False)
        amostra.loc[zeros, "price"] = "$0.00"
        # 2% dos nomes em branco; 4% dos anfitriões sem nome
        em_branco = self.rng.choice(n, int(0.02 * n), replace=False)
        amostra.loc[em_branco, "name"] = ""
        sem_nome = self.rng.choice(n, int(0.04 * n), replace=False)
        amostra.loc[sem_nome, "host_name"] = np.nan
        # 60 linhas copiadas por último: duplicatas exatas, como uma coleta repetida
        copias = amostra.sample(60, random_state=7)
        amostra = pd.concat([amostra, copias], ignore_index=True)
        return amostra.sample(frac=1, random_state=11).reset_index(drop=True)

    def salvar(self, amostra, caminho=SAIDA):
        caminho.parent.mkdir(parents=True, exist_ok=True)
        amostra.to_csv(caminho, index=False)
        return caminho

    def filtrar_calendario(self, caminho_calendario, ids, destino=SAIDA_CALENDARIO):
        """Mantém só as noites dos imóveis da amostra (o calendário completo tem ~17 milhões de linhas)."""
        partes = []
        for bloco in pd.read_csv(caminho_calendario, chunksize=1_000_000, low_memory=False):
            partes.append(bloco[bloco["listing_id"].isin(ids)])
        calendario = pd.concat(partes, ignore_index=True)
        destino.parent.mkdir(parents=True, exist_ok=True)
        calendario.to_csv(destino, index=False)
        return destino, len(calendario)

    def main(self, caminho_origem, caminho_calendario=None):
        dados = self.carregar(caminho_origem)
        amostra = self.pseudonimizar(self.amostrar(dados))
        ids = amostra["id"].unique()
        if caminho_calendario is not None:
            destino_cal, n_cal = self.filtrar_calendario(caminho_calendario, ids)
            print(f"Calendário da amostra salvo em {destino_cal} com {n_cal} linhas")
        amostra = self.injetar_problemas(amostra)
        destino = self.salvar(amostra)
        print(f"Amostra salva em {destino} com {len(amostra)} linhas e {amostra.shape[1]} colunas")


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit("Uso: python -m casos.airbnb.preparacao listings.csv.gz [calendar.csv.gz]")
    PreparadorAirbnb().main(*sys.argv[1:])
