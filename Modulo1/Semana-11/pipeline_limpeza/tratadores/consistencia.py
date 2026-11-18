"""Consistência: regras de negócio. Cada regra é uma máscara que diz quais linhas são válidas."""
import numpy as np
import pandas as pd

from pipeline_limpeza.tratadores.base import TratadorBase


class TratadorConsistencia(TratadorBase):
    def __init__(self, dados, registro=None, regras=None):
        super().__init__(dados, registro)
        self.regras = regras or {}

    def _invalidas(self, nome, regra):
        # Ausente não é valor inválido: só conta o que está preenchido e quebra a regra
        coluna = nome.split(":")[0]
        return (~regra(self.dados)) & self.dados[coluna].notna()

    def relatorio(self):
        return pd.Series({nome: int(self._invalidas(nome, regra).sum()) for nome, regra in self.regras.items()},
                         name="linhas_invalidas")

    def aplicar(self, colunas_nan=True):
        for nome, regra in self.regras.items():
            invalidas = self._invalidas(nome, regra)
            n = int(invalidas.sum())
            if n == 0:
                continue
            coluna = nome.split(":")[0]
            if colunas_nan:
                self.dados.loc[invalidas, coluna] = np.nan
                acao = f"{n} valores inválidos viraram NaN"
            else:
                self.dados = self.dados[~invalidas]
                acao = f"{n} linhas removidas"
            self._registrar(coluna, nome, acao, "regra de negócio: valor impossível não é informação")
        return self

    def executar(self):
        return self.aplicar().dados
