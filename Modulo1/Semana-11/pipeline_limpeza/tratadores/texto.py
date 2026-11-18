"""Texto: espaços sobrando, categorias raras e codificação de categorias (one-hot)."""
import numpy as np
import pandas as pd

from pipeline_limpeza.tratadores.base import TratadorBase


class TratadorTexto(TratadorBase):
    def limpar_espacos(self, colunas):
        for c in colunas:
            serie = self.dados[c].astype("string").str.replace(r"\s+", " ", regex=True).str.strip()
            self.dados[c] = serie.astype(object).where(serie.notna(), np.nan)
            self._registrar(c, "espaços sobrando", "removi espaços extras",
                            "'Copacabana ' e 'Copacabana' são o mesmo bairro")
        return self

    def agrupar_raras(self, coluna, minimo=30, rotulo="Outros", referencia=None):
        # 'referencia' = o treino: as categorias raras são decididas nele e aplicadas também ao teste
        base = self.dados if referencia is None else referencia
        contagem = base[coluna].value_counts()
        raras = contagem[contagem < minimo].index
        self.dados[coluna] = self.dados[coluna].where(~self.dados[coluna].isin(raras), rotulo)
        self._registrar(coluna, f"categorias com menos de {minimo} casos",
                        f"agrupei {len(raras)} categorias em '{rotulo}'", "evita colunas quase vazias no modelo")
        return self

    @staticmethod
    def dummies_treino_teste(treino, teste, colunas):
        # One-hot: as colunas são criadas no treino; o teste recebe as mesmas colunas (faltantes = 0)
        t = pd.get_dummies(treino, columns=colunas, dtype=int)
        s = pd.get_dummies(teste, columns=colunas, dtype=int).reindex(columns=t.columns, fill_value=0)
        return t, s

    def executar(self):
        colunas = self.dados.select_dtypes(include="object").columns.tolist()
        return self.limpar_espacos(colunas).dados
