"""Caminhos e regras do projeto. Todos os caminhos partem da raiz do projeto, não da pasta de execução."""
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent

DADOS_BRUTOS = RAIZ / "dados" / "brutos"            # o que chega da fonte, sem alteração
DADOS_PROCESSADOS = RAIZ / "dados" / "processados"  # o que o pipeline produz
DADOS_REFERENCIA = RAIZ / "dados" / "referencias"   # mapas e tabelas de apoio
SAIDAS_DECISOES = RAIZ / "saidas" / "decisoes"      # tabelas de decisões da limpeza
SAIDAS_ANALISES = RAIZ / "saidas" / "analises"      # tabelas e resumos das análises

def relativo(caminho):
    """Caminho relativo à raiz do projeto (para logs e saídas não mostrarem a pasta do computador)."""
    try:
        return Path(caminho).relative_to(RAIZ)
    except ValueError:
        return Path(caminho)


COLUNAS_OBRIGATORIAS = ["id", "price", "minimum_nights", "neighbourhood_cleansed", "room_type"]

# Regras de negócio da aula (hipóteses didáticas: discuta-as com a turma)
REGRAS_NEGOCIO = {
    "price: preço maior que zero": lambda d: pd.to_numeric(d["price"], errors="coerce") > 0,
    "minimum_nights: entre 1 e 365 noites": lambda d: d["minimum_nights"].between(1, 365),
    "accommodates: entre 1 e 16 hóspedes": lambda d: d["accommodates"].between(1, 16),
}
