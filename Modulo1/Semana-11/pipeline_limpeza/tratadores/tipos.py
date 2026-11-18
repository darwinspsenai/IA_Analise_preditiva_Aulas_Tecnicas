"""Tipos: número guardado como texto, data como texto e sim/não como letra."""
import pandas as pd

from pipeline_limpeza.tratadores.base import TratadorBase


class TratadorTipos(TratadorBase):
    def converter_numerico(self, coluna):
        original = self.dados[coluna].astype("string")
        limpo = original.str.replace(r"[$R\s]", "", regex=True).str.replace(",", "", regex=False)
        self.dados[coluna] = pd.to_numeric(limpo, errors="coerce")
        ruins = int(self.dados[coluna].isna().sum() - original.isna().sum())
        self._registrar(coluna, "número guardado como texto",
                        f"converti para número ({ruins} valores não convertidos viraram NaN)",
                        "sem isso não é possível calcular média nem gráfico")
        return self

    def converter_data(self, coluna):
        self.dados[coluna] = pd.to_datetime(self.dados[coluna], errors="coerce")
        self._registrar(coluna, "data guardada como texto", "converti para datetime (errors='coerce')",
                        "permite calcular intervalos de dias; datas inválidas viram NaT")
        return self

    def converter_booleano(self, coluna):
        self.dados[coluna] = self.dados[coluna].map({"t": True, "f": False})
        self._registrar(coluna, "sim/não como letra", "troquei 't'/'f' por True/False", "padrão booleano do pandas")
        return self

    def executar(self):
        return self.dados
