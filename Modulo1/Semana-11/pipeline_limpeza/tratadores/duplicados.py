"""Duplicados: a mesma coleta não pode contar duas vezes."""
from pipeline_limpeza.tratadores.base import TratadorBase


class TratadorDuplicados(TratadorBase):
    def contar(self, subset=None):
        return int(self.dados.duplicated(subset=subset).sum())

    def remover(self, subset=None, manter="first"):
        antes = len(self.dados)
        self.dados = self.dados.drop_duplicates(subset=subset, keep=manter)
        nome = "linha inteira" if subset is None else ", ".join(subset)
        self._registrar(nome, "registro repetido", "mantive a primeira ocorrência",
                        "a mesma coleta não pode contar duas vezes", antes)
        return self

    def executar(self):
        return self.remover(subset=None).dados
