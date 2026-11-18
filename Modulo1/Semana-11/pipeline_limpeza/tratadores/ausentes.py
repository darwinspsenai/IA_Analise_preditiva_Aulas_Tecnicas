"""Valores ausentes: padroniza a escrita de 'faltou', remove colunas vazias e preenche ou remove linhas."""
import numpy as np

from pipeline_limpeza.tratadores.base import TratadorBase


class TratadorAusentes(TratadorBase):
    VALORES_AUSENTES = ["", "não informado", "--", "-999", "N/A"]

    def padronizar_nulos(self, colunas=None):
        colunas = colunas or list(self.dados.columns)
        antes = self.dados[colunas].isna().sum().sum()
        for c in colunas:
            if self.dados[c].dtype == object:
                self.dados[c] = self.dados[c].replace(self.VALORES_AUSENTES, np.nan)
        depois = self.dados[colunas].isna().sum().sum()
        self._registrar("várias", "ausência escrita de formas diferentes",
                        f"troquei {depois - antes} textos por NaN", "um único código para 'faltou'")
        return self

    def remover_colunas_vazias(self, limite=1.0):
        vazias = [c for c in self.dados.columns if self.dados[c].isna().mean() >= limite]
        self.dados = self.dados.drop(columns=vazias)
        for c in vazias:
            self._registrar(c, "100% vazia", "removi a coluna", "não tem informação para nenhum imóvel")
        return self

    def preencher(self, coluna, valor, justificativa):
        """Preenche os ausentes de uma coluna com um valor e registra o porquê da escolha."""
        ausentes = int(self.dados[coluna].isna().sum())
        self.dados[coluna] = self.dados[coluna].fillna(valor)
        self._registrar(coluna, f"{ausentes} ausentes", f"preenchi com {valor!r}", justificativa)
        return self

    def remover_linhas_sem(self, coluna):
        antes = len(self.dados)
        self.dados = self.dados.dropna(subset=[coluna])
        self._registrar(coluna, "valor obrigatório ausente", "removi as linhas",
                        "sem a coluna a análise não existe", antes)
        return self

    def executar(self):
        return self.padronizar_nulos().remover_colunas_vazias().dados
