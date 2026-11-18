"""Gráficos da aula. Cada método chama um método de Visualizacao (visualizacao.py)."""
from pipeline_limpeza.analise import Analise
from pipeline_limpeza.visualizacao import Visualizacao


class Graficos(Analise):
    """Herda o diagnóstico de Analise e acrescenta os gráficos."""

    def histograma(self, coluna, titulo, bins=30, limite=None):
        Visualizacao.histograma(self.dados, coluna, titulo, bins=bins, limite=limite)

    def boxplot(self, coluna, titulo, grupo=None, limite=None):
        Visualizacao.boxplot(self.dados, coluna, titulo, grupo=grupo, limite=limite)

    def barras_por_grupo(self, grupo, valor, titulo, horizontal=False):
        tabela = self.dados.groupby(grupo)[valor].count().sort_values(ascending=False).head(10)
        Visualizacao.barras_serie(tabela, titulo, horizontal=horizontal, rotulo_valor="Quantidade")

    def percentual_ausentes(self, titulo):
        Visualizacao.percentual_ausentes(self.dados, titulo)

    def barras_serie(self, serie, titulo, fmt="%.0f", horizontal=False):
        Visualizacao.barras_serie(serie, titulo, fmt=fmt, horizontal=horizontal)

    def dispersao(self, x, y, titulo):
        Visualizacao.dispersao(self.dados, x, y, titulo)

    def comparar_histogramas(self, antes, depois, coluna, limite=None):
        Visualizacao.comparar_histogramas(antes, depois, coluna, "Sem limpeza", "Com limpeza", limite=limite)

    def comparar_boxplots(self, antes, depois, coluna, grupo=None, limite=None):
        Visualizacao.comparar_boxplots(antes, depois, coluna, "Sem limpeza", "Com limpeza",
                                       grupo=grupo, limite=limite)

    def comparar_barras(self, antes, depois, titulo, fmt="%.0f"):
        Visualizacao.comparar_barras(antes, depois, titulo, "Sem limpeza", "Com limpeza", fmt=fmt,
                                     rotulo_valor="Preço médio (R$)")
