"""Validação do esquema: falha cedo, com mensagem clara, quando faltam colunas."""
from pipeline_limpeza.config import COLUNAS_OBRIGATORIAS


class ValidadorEsquema:
    def __init__(self, colunas_obrigatorias=COLUNAS_OBRIGATORIAS):
        self.colunas_obrigatorias = list(colunas_obrigatorias)

    def validar(self, dados):
        faltam = [c for c in self.colunas_obrigatorias if c not in dados.columns]
        if faltam:
            raise ValueError(f"Esquema inválido: faltam as colunas {faltam}. "
                             f"Verifique se o arquivo é o listings.csv da cidade certa.")
        return dados
