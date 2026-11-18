"""Diagnóstico de um DataFrame: mede e descreve, sem alterar os dados."""
import pandas as pd


class Analise:
    def __init__(self, dados, nome="base"):
        self.dados = dados.copy()
        self.nome = nome

    def resumo(self):
        return {"linhas": self.dados.shape[0], "colunas": self.dados.shape[1],
                "linhas_duplicadas": int(self.dados.duplicated().sum()),
                "celulas_vazias": int(self.dados.isna().sum().sum())}

    def diagnostico(self):
        tabela = pd.DataFrame({
            "tipo": self.dados.dtypes.astype(str),
            "ausentes": self.dados.isna().sum(),
            "pct_ausentes": (self.dados.isna().mean() * 100).round(1),
            "valores_unicos": self.dados.nunique(),
        })
        return tabela.sort_values("pct_ausentes", ascending=False)

    def estatisticas(self, coluna):
        serie = pd.to_numeric(self.dados[coluna], errors="coerce")
        return {"média": round(serie.mean(), 2), "mediana": round(serie.median(), 2),
                "desvio": round(serie.std(), 2), "mínimo": serie.min(), "máximo": serie.max(),
                "n": int(serie.notna().sum())}

    def tabela_media_mediana(self, coluna, grupo=None):
        serie = pd.to_numeric(self.dados[coluna], errors="coerce")
        if grupo is None:
            return pd.DataFrame({"média": [serie.mean()], "mediana": [serie.median()]}, index=[coluna])
        dados = pd.DataFrame({grupo: self.dados[grupo], coluna: serie})
        return dados.groupby(grupo)[coluna].agg(["count", "mean", "median"]).round(2)
