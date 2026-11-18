"""Importação: lê um CSV (também .csv.gz) e valida o esquema antes de qualquer tratamento."""
import logging
from pathlib import Path

import pandas as pd

from pipeline_limpeza.config import relativo

logger = logging.getLogger("pipeline")


class LeitorDados:
    def __init__(self, validador=None):
        self.validador = validador

    def ler(self, caminho, colunas=None):
        caminho = Path(caminho)
        if not caminho.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}. Confira a pasta de trabalho.")
        dados = pd.read_csv(caminho, low_memory=False, usecols=colunas)  # compressão pela extensão
        logger.info("lido %s: %d linhas, %d colunas", relativo(caminho), *dados.shape)
        if self.validador is not None:
            self.validador.validar(dados)
        return dados
