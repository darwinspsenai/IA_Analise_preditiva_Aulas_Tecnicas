"""Outliers pelo IQR: marcar, limitar (capping) ou remover."""
import pandas as pd

from pipeline_limpeza.tratadores.base import TratadorBase


class TratadorOutliers(TratadorBase):
    def __init__(self, dados, registro=None, fator=1.5):
        super().__init__(dados, registro)
        self.fator = fator

    def limites(self, coluna):
        serie = pd.to_numeric(self.dados[coluna], errors="coerce").dropna()
        q1, q3 = serie.quantile(0.25), serie.quantile(0.75)
        iqr = q3 - q1
        return {"Q1": q1, "Q3": q3, "IQR": iqr,
                "inferior": q1 - self.fator * iqr, "superior": q3 + self.fator * iqr}

    def marcar(self, coluna):
        lim = self.limites(coluna)
        serie = pd.to_numeric(self.dados[coluna], errors="coerce")
        return (serie < lim["inferior"]) | (serie > lim["superior"])

    def limitar(self, coluna):
        """Capping: os valores extremos viram o limite, sem apagar a linha."""
        lim = self.limites(coluna)
        n = int(self.marcar(coluna).sum())
        self.dados[coluna] = pd.to_numeric(self.dados[coluna], errors="coerce").clip(lim["inferior"], lim["superior"])
        self._registrar(coluna, f"outliers pelo IQR (fator {self.fator})",
                        f"limitei {n} valores aos limites", "mantém a linha e reduz o efeito do extremo")
        return self

    def remover(self, coluna):
        antes = len(self.dados)
        self.dados = self.dados[~self.marcar(coluna)]
        self._registrar(coluna, f"outliers pelo IQR (fator {self.fator})", "removi as linhas",
                        "muda a população estudada: documente", antes)
        return self

    def executar(self):
        return self.dados
