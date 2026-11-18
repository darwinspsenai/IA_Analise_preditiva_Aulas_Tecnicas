"""Pipeline de limpeza: ler -> validar -> limpar -> exportar. Reexecutar dá o mesmo resultado."""
import logging

from pipeline_limpeza.config import REGRAS_NEGOCIO, SAIDAS_DECISOES
from pipeline_limpeza.exportacao import ExportadorDados
from pipeline_limpeza.leitura import LeitorDados
from pipeline_limpeza.registro import RegistroDecisoes
from pipeline_limpeza.tratadores import (TratadorAusentes, TratadorConsistencia, TratadorDuplicados,
                                         TratadorOutliers, TratadorTexto, TratadorTipos, TratadorUnidades)
from pipeline_limpeza.validacao import ValidadorEsquema

logger = logging.getLogger("pipeline")


class PipelineLimpeza:
    """Cada etapa usa uma classe de tratamento. A exportação sabe em qual pasta gravar."""

    def __init__(self, exportador=None, exportador_decisoes=None):
        self.registro = RegistroDecisoes()
        self.validador = ValidadorEsquema()
        self.leitor = LeitorDados(self.validador)
        self.exportador = exportador or ExportadorDados()
        self.exportador_decisoes = exportador_decisoes or ExportadorDados(SAIDAS_DECISOES)

    def limpar(self, bruto):
        dados = bruto.copy()
        linhas = len(dados)
        dados = TratadorAusentes(dados, self.registro).padronizar_nulos().remover_colunas_vazias().dados
        dados = TratadorTipos(dados, self.registro).converter_numerico("price").dados
        dados = TratadorTexto(dados, self.registro).limpar_espacos(["name", "host_name"]).dados
        dados = TratadorTipos(dados, self.registro).converter_data("last_review").dados
        dados = TratadorUnidades(dados, self.registro).extrair_banheiros().dados
        dados = TratadorDuplicados(dados, self.registro).remover().dados
        dados = TratadorConsistencia(dados, self.registro, regras=REGRAS_NEGOCIO).aplicar().dados
        dados = TratadorOutliers(dados, self.registro).limitar("price").dados
        logger.info("linhas: %d -> %d", linhas, len(dados))
        return dados

    def exportar(self, limpos, nome="airbnb_rio_limpo.csv"):
        caminho = self.exportador.exportar(limpos, nome)
        self.exportador_decisoes.exportar(self.registro.tabela(), "decisoes_limpeza.csv")
        return caminho

    def executar(self, caminho_bruto, nome_saida="airbnb_rio_limpo.csv"):
        bruto = self.leitor.ler(caminho_bruto)
        limpos = self.limpar(bruto)
        self.exportar(limpos, nome_saida)
        return limpos
