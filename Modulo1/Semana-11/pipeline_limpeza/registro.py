"""Registro das decisões da limpeza: coluna, problema, ação e justificativa (aula 3.6)."""
from pathlib import Path

import pandas as pd


class RegistroDecisoes:
    def __init__(self):
        self.linhas = []

    def adicionar(self, coluna, problema, acao, justificativa, linhas_removidas=0):
        self.linhas.append({"coluna": coluna, "problema": problema, "acao": acao,
                            "justificativa": justificativa, "linhas_removidas": linhas_removidas})

    def tabela(self):
        return pd.DataFrame(self.linhas)

    def exportar(self, caminho):
        Path(caminho).parent.mkdir(parents=True, exist_ok=True)
        self.tabela().to_csv(caminho, index=False, encoding="utf-8")
        return caminho
