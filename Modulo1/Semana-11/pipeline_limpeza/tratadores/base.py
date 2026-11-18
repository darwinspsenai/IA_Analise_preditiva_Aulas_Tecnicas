"""Base dos tratadores: cada um recebe um DataFrame, altera uma cópia e registra o que fez."""
import logging
from abc import ABC, abstractmethod

from pipeline_limpeza.registro import RegistroDecisoes

logger = logging.getLogger("pipeline")


class TratadorBase(ABC):
    def __init__(self, dados, registro=None):
        self.dados = dados.copy()
        self.registro = registro if registro is not None else RegistroDecisoes()

    def _registrar(self, coluna, problema, acao, justificativa, linhas_antes=None):
        removidas = 0 if linhas_antes is None else linhas_antes - len(self.dados)
        self.registro.adicionar(coluna, problema, acao, justificativa, removidas)
        logger.info("%s | %s: %s (linhas removidas: %d)", type(self).__name__, coluna, acao, removidas)

    @abstractmethod
    def executar(self):
        """Aplica o tratamento padrão da classe e devolve o DataFrame."""
