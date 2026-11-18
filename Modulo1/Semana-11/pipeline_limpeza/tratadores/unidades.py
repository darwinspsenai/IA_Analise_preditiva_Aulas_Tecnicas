"""Unidades: separa número e unidade (ex.: '1.5 baths' -> 1.5) e converte medidas para a mesma escala."""
import numpy as np

from pipeline_limpeza.tratadores.base import TratadorBase


class TratadorUnidades(TratadorBase):
    def extrair_banheiros(self, coluna="bathrooms_text", nova="banheiros"):
        texto = self.dados[coluna].astype("string").str.lower()
        numero = texto.str.extract(r"(\d+(?:\.\d+)?)")[0].astype(float)
        meio = texto.str.contains("half", na=False)
        # sem número e com "half" (ex.: 'Half-bath') vale 0,5; com número, vale o número
        self.dados[nova] = numero.where(numero.notna(), np.where(meio, 0.5, np.nan))
        self.dados["banheiro_compartilhado"] = texto.str.contains("shared", na=False)
        self._registrar(coluna, "número e unidade no mesmo texto",
                        f"criei '{nova}' e 'banheiro_compartilhado'", "uma coluna por informação")
        return self

    def converter_medida(self, coluna, fatores, nova):
        """fatores: dicionário {unidade: multiplicador}, ex.: {'g': 0.001, 'kg': 1}."""
        valor = self.dados[coluna]
        self.dados[nova] = valor * self.dados["unidade"].map(fatores)
        self._registrar(coluna, "unidades diferentes", f"converti para a mesma unidade em '{nova}'",
                        "compara-se apenas medidas na mesma escala")
        return self

    def executar(self):
        return self.extrair_banheiros().dados
