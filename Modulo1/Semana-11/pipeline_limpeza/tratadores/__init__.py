"""Tratadores: cada arquivo trata um tipo de problema e herda de TratadorBase."""
from pipeline_limpeza.tratadores.ausentes import TratadorAusentes
from pipeline_limpeza.tratadores.base import TratadorBase
from pipeline_limpeza.tratadores.consistencia import TratadorConsistencia
from pipeline_limpeza.tratadores.duplicados import TratadorDuplicados
from pipeline_limpeza.tratadores.imputacao import ImputadorAusentes
from pipeline_limpeza.tratadores.outliers import TratadorOutliers
from pipeline_limpeza.tratadores.texto import TratadorTexto
from pipeline_limpeza.tratadores.tipos import TratadorTipos
from pipeline_limpeza.tratadores.unidades import TratadorUnidades

__all__ = ["TratadorBase", "TratadorAusentes", "TratadorTexto", "TratadorTipos", "TratadorUnidades",
           "TratadorDuplicados", "TratadorConsistencia", "ImputadorAusentes", "TratadorOutliers"]
