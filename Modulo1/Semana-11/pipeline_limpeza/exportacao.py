"""Exportação: grava tabelas na pasta que a própria classe conhece (o formato sai do nome do arquivo)."""
import logging
from pathlib import Path

from pipeline_limpeza.config import DADOS_PROCESSADOS, relativo

logger = logging.getLogger("pipeline")


class ExportadorDados:
    def __init__(self, pasta=DADOS_PROCESSADOS):
        self.pasta = Path(pasta)

    def exportar(self, dados, nome):
        self.pasta.mkdir(parents=True, exist_ok=True)
        caminho = self.pasta / nome
        if nome.endswith(".json"):
            dados.to_json(caminho, orient="records", force_ascii=False, indent=2)
        else:
            dados.to_csv(caminho, index=False)  # csv ou csv.gz
        logger.info("exportado %s: %d linhas", relativo(caminho), len(dados))
        return relativo(caminho)
