"""Pacote do pipeline de limpeza de dados (aula Pipelines de Dados em Python).

Um arquivo por responsabilidade:
  config.py         caminhos, colunas obrigatórias e regras de negócio
  leitura.py        LeitorDados: importa CSV e CSV.GZ e valida o esquema
  validacao.py      ValidadorEsquema: falha cedo se faltam colunas
  exportacao.py     ExportadorDados: grava CSV, CSV.GZ ou JSON na pasta que a classe conhece
  registro.py       RegistroDecisoes: tabela "coluna, problema, ação, justificativa"
  analise.py        Analise: diagnóstico, sem alterar os dados
  graficos.py       Graficos(Analise): gráficos da aula
  visualizacao.py   Visualizacao: funções de desenho (matplotlib e seaborn)
  tratadores/       um tratador por problema (ausentes, texto, tipos, unidades, duplicados,
                    consistência, outliers) e o imputador, todos herdando de TratadorBase
  preparacao.py     Escalonador e DivisorTreinoTeste (preparação para modelagem)
  pipeline.py       PipelineLimpeza: lê, valida, limpa e exporta, com logging

Uso típico:
    from pipeline_limpeza import PipelineLimpeza
    limpos = PipelineLimpeza().executar('dados/brutos/airbnb_rio_bruto.csv')
"""
import logging

from pipeline_limpeza.analise import Analise
from pipeline_limpeza.exportacao import ExportadorDados
from pipeline_limpeza.graficos import Graficos
from pipeline_limpeza.leitura import LeitorDados
from pipeline_limpeza.pipeline import PipelineLimpeza
from pipeline_limpeza.preparacao import DivisorTreinoTeste, Escalonador
from pipeline_limpeza.registro import RegistroDecisoes
from pipeline_limpeza.tratadores import (ImputadorAusentes, TratadorAusentes, TratadorBase,
                                         TratadorConsistencia, TratadorDuplicados, TratadorOutliers,
                                         TratadorTexto, TratadorTipos, TratadorUnidades)
from pipeline_limpeza.validacao import ValidadorEsquema

logger = logging.getLogger("pipeline")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")

__all__ = [
    "Analise", "ExportadorDados", "Graficos", "LeitorDados", "PipelineLimpeza",
    "DivisorTreinoTeste", "Escalonador", "RegistroDecisoes", "ValidadorEsquema",
    "ImputadorAusentes", "TratadorAusentes", "TratadorBase", "TratadorConsistencia",
    "TratadorDuplicados", "TratadorOutliers", "TratadorTexto", "TratadorTipos", "TratadorUnidades",
]
