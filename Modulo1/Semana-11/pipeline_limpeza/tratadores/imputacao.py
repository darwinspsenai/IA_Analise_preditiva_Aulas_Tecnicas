"""Imputação: aprende o valor de preenchimento no TREINO e aplica em treino e teste (sem vazamento)."""
import pandas as pd

from pipeline_limpeza.tratadores.base import TratadorBase


class ImputadorAusentes(TratadorBase):
    def __init__(self, dados=None, registro=None):
        super().__init__(dados if dados is not None else pd.DataFrame(), registro)
        self.valores = {}

    def ajustar(self, treino, colunas, estrategia="mediana"):
        for c in colunas:
            if estrategia == "mediana":
                self.valores[c] = pd.to_numeric(treino[c], errors="coerce").median()
            elif estrategia == "moda":
                self.valores[c] = treino[c].mode(dropna=True).iloc[0]
            else:
                raise ValueError("estrategia deve ser 'mediana' ou 'moda'")
        return self

    def transformar(self, dados):
        resultado = dados.copy()
        for c, valor in self.valores.items():
            resultado[c] = resultado[c].fillna(valor)
        return resultado

    def ajustar_transformar(self, treino, colunas, estrategia="mediana"):
        return self.ajustar(treino, colunas, estrategia).transformar(treino)

    def executar(self):
        return self.dados
