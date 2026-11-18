"""Gráficos das aulas de limpeza de dados, reunidos na classe Visualizacao.

Todos os métodos são estáticos: recebem um DataFrame ou uma Series e mostram o gráfico com plt.show().
Para comparar ANTES e DEPOIS da limpeza use os métodos comparar_*: eles desenham os
dois gráficos lado a lado, com a mesma escala, para a comparação ser justa.

Métodos:
  histograma, boxplot, barras_serie, barras, dispersao, linhas, pizza,
  mapa_ausentes, percentual_ausentes, mapa_calor,
  comparar_histogramas, comparar_boxplots, comparar_barras, mapa_calor_no_mapa
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap
from matplotlib.patches import PathPatch
from matplotlib.path import Path as MplPath
TEAL = "#2A7F87"
CLARO = "#8FC1C6"
VERMELHO = "#B5523B"
CINZA = "#5B6B72"
sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams.update({
    "figure.figsize": (8, 4), "font.size": 11,
    "axes.facecolor": "#F7FAFC", "figure.facecolor": "white",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titleweight": "bold", "axes.titlesize": 13, "axes.titlepad": 14,
    "grid.alpha": 0.28, "grid.color": "#A6BBC7", "axes.edgecolor": "#CBD5DD",
})


class Visualizacao:
    """Gráficos das aulas de limpeza de dados. Todos os métodos são estáticos: recebem os dados e o título."""

    @staticmethod
    def _rotulo(texto):
        return str(texto).replace("_", " ").capitalize()

    @staticmethod
    def _estilo(ax, titulo, xlabel=None, ylabel=None):
        ax.set_title(titulo)
        if xlabel is not None:
            ax.set_xlabel(xlabel)
        if ylabel is not None:
            ax.set_ylabel(ylabel)

    @staticmethod
    def _finalizar(fig):
        fig.tight_layout()
        plt.show()

    @staticmethod
    def _hist(ax, dados, coluna, titulo, bins=30, cor=TEAL, limite=None):
        sns.histplot(data=dados, x=coluna, bins=bins, color=cor,
                     edgecolor="white", linewidth=0.4, ax=ax)
        Visualizacao._estilo(ax, titulo, Visualizacao._rotulo(coluna), "Quantidade de pedidos")
        if limite is not None:
            ax.set_xlim(*limite)

    @staticmethod
    def histograma(dados, coluna, titulo, bins=30, limite=None):
        fig, ax = plt.subplots()
        Visualizacao._hist(ax, dados, coluna, titulo, bins, TEAL, limite)
        Visualizacao._finalizar(fig)

    @staticmethod
    def _box(ax, dados, coluna, titulo, grupo=None, limite=None):
        if grupo is None:
            sns.boxplot(data=dados, x=coluna, color=CLARO, width=0.5,
                        flierprops={"marker": "o", "markersize": 4, "alpha": 0.6}, ax=ax)
            Visualizacao._estilo(ax, titulo, Visualizacao._rotulo(coluna))
            if limite is not None:
                ax.set_xlim(*limite)
        else:
            sns.boxplot(data=dados, x=coluna, y=grupo, color=CLARO, width=0.6,
                        flierprops={"marker": "o", "markersize": 4, "alpha": 0.6}, ax=ax)
            Visualizacao._estilo(ax, titulo, Visualizacao._rotulo(coluna), Visualizacao._rotulo(grupo))
            if limite is not None:
                ax.set_xlim(*limite)

    @staticmethod
    def boxplot(dados, coluna, titulo, grupo=None, limite=None):
        """Boxplot de uma coluna; com grupo, um boxplot por categoria."""
        altura = 3.6 if grupo is None else 4.5
        fig, ax = plt.subplots(figsize=(8, altura))
        Visualizacao._box(ax, dados, coluna, titulo, grupo, limite)
        Visualizacao._finalizar(fig)

    @staticmethod
    def comparar_histogramas(antes, depois, coluna, titulo_antes="Antes",
                             titulo_depois="Depois", bins=30, limite=None):
        """Dois histogramas lado a lado, com o mesmo eixo X e o mesmo eixo Y."""
        fig, eixos = plt.subplots(1, 2, figsize=(11, 4), sharex=True, sharey=True)
        Visualizacao._hist(eixos[0], antes, coluna, titulo_antes, bins, VERMELHO, limite)
        Visualizacao._hist(eixos[1], depois, coluna, titulo_depois, bins, TEAL, limite)
        Visualizacao._finalizar(fig)

    @staticmethod
    def comparar_boxplots(antes, depois, coluna, titulo_antes="Antes",
                          titulo_depois="Depois", grupo=None, limite=None):
        """Dois boxplots lado a lado, com a mesma escala."""
        altura = 3.8 if grupo is None else 5
        fig, eixos = plt.subplots(1, 2, figsize=(12, altura), sharex=True)
        Visualizacao._box(eixos[0], antes, coluna, titulo_antes, grupo, limite)
        Visualizacao._box(eixos[1], depois, coluna, titulo_depois, grupo, limite)
        if grupo is not None:
            eixos[1].set_ylabel("")
        Visualizacao._finalizar(fig)

    @staticmethod
    def _barras_serie(ax, serie, titulo, fmt="%.0f", horizontal=False, rotulo_valor="Quantidade"):
        nomes = [str(i) for i in serie.index]
        if horizontal:
            barras = ax.barh(nomes, serie.values, color=TEAL, height=0.65)
            ax.bar_label(barras, fmt=fmt, padding=4, fontsize=10)
            ax.margins(x=0.15)
            Visualizacao._estilo(ax, titulo, rotulo_valor, None)
            ax.grid(axis="y", visible=False)
        else:
            barras = ax.bar(nomes, serie.values, color=TEAL, width=0.65)
            ax.bar_label(barras, fmt=fmt, padding=3, fontsize=10)
            ax.margins(y=0.15)
            Visualizacao._estilo(ax, titulo, None, rotulo_valor)
            ax.tick_params(axis="x", labelrotation=25)
            ax.grid(axis="x", visible=False)

    @staticmethod
    def barras_serie(serie, titulo, fmt="%.0f", horizontal=False, rotulo_valor="Quantidade"):
        fig, ax = plt.subplots()
        Visualizacao._barras_serie(ax, serie, titulo, fmt, horizontal, rotulo_valor)
        Visualizacao._finalizar(fig)

    @staticmethod
    def barras(tabela, categoria, valor, titulo, horizontal=False):
        """Barras de uma coluna numérica por categoria (já agregada ou não)."""
        fig, ax = plt.subplots()
        if horizontal:
            sns.barplot(data=tabela, x=valor, y=categoria, color=TEAL, errorbar=None, ax=ax)
        else:
            sns.barplot(data=tabela, x=categoria, y=valor, color=TEAL, errorbar=None, ax=ax)
        for grupo in ax.containers:
            ax.bar_label(grupo, fmt="%.1f", padding=3, fontsize=10)
        Visualizacao._estilo(ax, titulo, Visualizacao._rotulo(valor if horizontal else categoria),
                Visualizacao._rotulo(categoria if horizontal else valor))
        Visualizacao._finalizar(fig)

    @staticmethod
    def pizza(tabela, rotulo, valor, titulo=None):
        fig, ax = plt.subplots()
        ax.pie(tabela[valor], labels=tabela[rotulo], autopct="%1.1f%%", startangle=90,
               pctdistance=0.7, wedgeprops={"edgecolor": "white", "linewidth": 2},
               textprops={"color": "#23373B", "fontsize": 11})
        ax.axis("equal")
        ax.set_title(titulo)
        Visualizacao._finalizar(fig)

    @staticmethod
    def mapa_calor(tabela, titulo, fmt="d"):
        """Mapa de calor de uma tabela cruzada (ex.: pd.crosstab)."""
        fig, ax = plt.subplots(figsize=(8, 4.5))
        sns.heatmap(tabela, annot=True, fmt=fmt, cmap="YlGnBu", linewidths=0.5,
                    linecolor="white", cbar=False, ax=ax)
        Visualizacao._estilo(ax, titulo, None, None)
        Visualizacao._finalizar(fig)

    @staticmethod
    def mapa_calor_no_mapa(valores, bordas_x, bordas_y, contornos, titulo, rotulo_valor="Valor"):
        """Mapa de calor encaixado no contorno da cidade.
        valores: matriz (linhas = faixas de latitude, do sul para o norte; colunas = faixas de longitude);
        bordas_x e bordas_y: limites das faixas; contornos: lista de anéis (N x 2, longitude e latitude)."""
        fig, ax = plt.subplots(figsize=(7.5, 8.2))
        malha = ax.pcolormesh(bordas_x, bordas_y, np.ma.masked_invalid(valores),
                              cmap="YlGnBu", shading="flat", alpha=0.92)
        recorte = PathPatch(MplPath.make_compound_path(*[MplPath(c) for c in contornos]), transform=ax.transData)
        malha.set_clip_path(recorte)
        ax.add_collection(LineCollection(contornos, colors=CINZA, linewidths=0.45))
        ax.set_xlim(bordas_x[0], bordas_x[-1])
        ax.set_ylim(bordas_y[0], bordas_y[-1])
        ax.set_aspect(1 / np.cos(np.deg2rad(np.mean(bordas_y))))  # proporção real de longitude e latitude
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        ax.spines[:].set_visible(False)
        fig.colorbar(malha, ax=ax, label=rotulo_valor, shrink=0.75)
        ax.set_title(titulo)
        Visualizacao._finalizar(fig)

    @staticmethod
    def comparar_barras(antes, depois, titulo, rotulo_antes="Antes", rotulo_depois="Depois",
                        fmt="%.0f", horizontal=False, rotulo_valor="Valor"):
        """Barras agrupadas: a mesma categoria antes e depois da limpeza."""
        tabela = pd.DataFrame({rotulo_antes: antes, rotulo_depois: depois}).fillna(0)
        x = np.arange(len(tabela))
        largura = 0.4
        fig, ax = plt.subplots(figsize=(10, 4.2))
        b1 = ax.bar(x - largura / 2, tabela[rotulo_antes], largura, color=VERMELHO, label=rotulo_antes)
        b2 = ax.bar(x + largura / 2, tabela[rotulo_depois], largura, color=TEAL, label=rotulo_depois)
        ax.set_xticks(x)
        ax.set_xticklabels([str(i) for i in tabela.index], rotation=25, ha="right")
        ax.bar_label(b1, fmt=fmt, padding=2, fontsize=9)
        ax.bar_label(b2, fmt=fmt, padding=2, fontsize=9)
        ax.margins(y=0.15)
        ax.legend(frameon=False)
        Visualizacao._estilo(ax, titulo, None, rotulo_valor)
        Visualizacao._finalizar(fig)

    @staticmethod
    def dispersao(dados, x, y, titulo, hue=None):
        fig, ax = plt.subplots()
        if hue is None:
            sns.scatterplot(data=dados, x=x, y=y, alpha=0.45, s=30, color=TEAL,
                            edgecolor="white", linewidth=0.3, ax=ax)
        else:
            sns.scatterplot(data=dados, x=x, y=y, hue=hue, alpha=0.6, s=30,
                            edgecolor="white", linewidth=0.3, palette="Set2", ax=ax)
        Visualizacao._estilo(ax, titulo, Visualizacao._rotulo(x), Visualizacao._rotulo(y))
        Visualizacao._finalizar(fig)

    @staticmethod
    def linhas(tabela, x, y, titulo=None, marcador="o", rotulo_x=None, rotulo_y=None, tamanho=None):
        fig, ax = plt.subplots(figsize=tamanho)
        sns.lineplot(data=tabela, x=x, y=y, marker=marcador, markersize=7,
                     linewidth=1.8, color=TEAL, ax=ax)
        Visualizacao._estilo(ax, titulo, rotulo_x or Visualizacao._rotulo(x), rotulo_y or Visualizacao._rotulo(y))
        fig.autofmt_xdate()
        Visualizacao._finalizar(fig)

    @staticmethod
    def mapa_ausentes(dados, titulo, max_linhas=400):
        """Cada linha do gráfico é uma coluna; vermelho = valor ausente."""
        faltantes = dados.isna()
        colunas = faltantes.columns[faltantes.any()]
        amostra = faltantes[colunas].sample(min(max_linhas, len(dados)), random_state=1).sort_index()
        fig, ax = plt.subplots(figsize=(9, 4.5))
        sns.heatmap(amostra.T.astype(int), cmap=ListedColormap(["#EDF5F6", VERMELHO]),
                    cbar=False, xticklabels=False, linewidths=0, ax=ax)
        Visualizacao._estilo(ax, titulo, f"{len(amostra)} linhas (amostra aleatória)", None)
        Visualizacao._finalizar(fig)

    @staticmethod
    def percentual_ausentes(dados, titulo):
        pct = dados.isna().mean().mul(100).sort_values(ascending=False)
        pct = pct[pct > 0].round(1)
        fig, ax = plt.subplots(figsize=(8, 4.2))
        Visualizacao._barras_serie(ax, pct, titulo, fmt="%.1f%%", horizontal=True, rotulo_valor="% de valores ausentes")
        Visualizacao._finalizar(fig)

    @staticmethod
    def pizza_lado_a_lado(antes, depois, titulo_antes, titulo_depois, cores):
        """Duas pizzas lado a lado. 'cores' liga cada rótulo a uma cor fixa; rótulos sem cor ficam cinza."""
        fig, eixos = plt.subplots(1, 2, figsize=(11, 5.2))
        for ax, dados, titulo in [(eixos[0], antes, titulo_antes), (eixos[1], depois, titulo_depois)]:
            ax.pie(dados, colors=[cores.get(r, "#8a949a") for r in dados.index], startangle=90, counterclock=False,
                   autopct="%1.1f%%", pctdistance=1.14, wedgeprops={"edgecolor": "white", "linewidth": 2},
                   textprops={"color": "#1d2a2e", "fontsize": 10})
            ax.legend([f"{r} ({n})" for r, n in dados.items()], loc="upper center", bbox_to_anchor=(0.5, -0.02),
                      ncol=2, frameon=False, fontsize=9)
            ax.set_title(titulo)
            ax.axis("equal")
        Visualizacao._finalizar(fig)

    @staticmethod
    def barras_lado_a_lado(antes, depois, titulo_antes, titulo_depois, cores):
        """Barras horizontais em dois painéis, cada um com a sua escala (compare a ordem, não a altura)."""
        fig, eixos = plt.subplots(1, 2, figsize=(12, 4.6))
        for ax, serie, titulo in [(eixos[0], antes.sort_values(), titulo_antes),
                                  (eixos[1], depois.sort_values(), titulo_depois)]:
            barras = ax.barh(serie.index, serie.values, color=[cores.get(r, "#8a949a") for r in serie.index])
            ax.bar_label(barras, fmt="%d", padding=3, fontsize=9)
            ax.margins(x=0.15)
            ax.set_title(titulo)
            ax.set_xlabel("Pedidos")
        Visualizacao._finalizar(fig)

    @staticmethod
    def linhas_empilhadas(antes, depois, titulo_antes, titulo_depois, cor_antes, cor_depois, ylabel):
        """Duas séries mensais (índice PeriodIndex), uma sobre a outra, cada uma com a sua escala."""
        fig, eixos = plt.subplots(2, 1, figsize=(10, 6.2), sharex=True)
        for ax, serie, cor, titulo in [(eixos[0], antes, cor_antes, titulo_antes),
                                       (eixos[1], depois, cor_depois, titulo_depois)]:
            ax.plot(serie.index.to_timestamp(), serie.values, marker="o", markersize=5, linewidth=1.8, color=cor)
            ax.set_title(titulo, loc="left")
            ax.set_ylabel(ylabel)
            ax.set_ylim(0, serie.max() * 1.15)
        eixos[1].set_xlabel("Mês do envio")
        fig.autofmt_xdate()
        Visualizacao._finalizar(fig)

    @staticmethod
    def linhas_comparadas(antes, depois, titulo, rotulo_antes, rotulo_depois, cor_antes, cor_depois, ylabel):
        """Duas séries mensais no mesmo eixo. Use só quando as duas medem a mesma coisa (ex.: dias)."""
        fig, ax = plt.subplots(figsize=(10, 4.6))
        ax.plot(antes.index.to_timestamp(), antes.values, marker="o", markersize=5, linewidth=1.8,
                color=cor_antes, label=rotulo_antes)
        ax.plot(depois.index.to_timestamp(), depois.values, marker="o", markersize=5, linewidth=1.8,
                color=cor_depois, label=rotulo_depois)
        ax.set_ylim(0, None)
        Visualizacao._estilo(ax, titulo, "Mês do envio", ylabel)
        ax.legend(frameon=False)
        fig.autofmt_xdate()
        Visualizacao._finalizar(fig)

    @staticmethod
    def matriz_dispersao(dados, colunas, hue, cores, titulo):
        """Matriz de dispersão com a metade inferior; a cor separa os grupos de 'hue'. 'cores': grupo -> cor."""
        g = sns.pairplot(dados[colunas + [hue]], hue=hue, corner=True, height=1.9, palette=cores,
                         plot_kws={"s": 14, "alpha": 0.5, "linewidth": 0},
                         diag_kws={"alpha": 0.6, "linewidth": 0})
        g.figure.suptitle(titulo, y=1.02, fontweight="bold")
        plt.show()

    @staticmethod
    def grade_dispersoes(dados, alvos, entradas, titulo, cor):
        """Uma linha por variável-alvo e uma coluna por variável de entrada; cada gráfico tem a sua escala."""
        fig, eixos = plt.subplots(len(alvos), len(entradas), figsize=(15, 6.8))
        for i, y in enumerate(alvos):
            for j, x in enumerate(entradas):
                ax = eixos[i, j]
                pares = dados[[x, y]].apply(pd.to_numeric, errors="coerce").dropna()
                ax.scatter(pares[x], pares[y], s=10, alpha=0.4, color=cor, linewidths=0)
                ax.set_xlabel(x.replace("_", " "))
                ax.set_ylabel(y.replace("_", " ") if j == 0 else "")
                ax.grid(alpha=0.25)
        fig.suptitle(titulo, fontweight="bold")
        Visualizacao._finalizar(fig)

    @staticmethod
    def mapas_correlacao(antes, depois, titulo_antes, titulo_depois):
        """Dois mapas de calor de correlação na mesma escala, de -1 a 1."""
        fig, eixos = plt.subplots(1, 2, figsize=(14, 6))
        for ax, tabela, titulo in [(eixos[0], antes, titulo_antes), (eixos[1], depois, titulo_depois)]:
            sns.heatmap(tabela, vmin=-1, vmax=1, center=0, cmap="RdBu_r", annot=True, fmt=".2f",
                        linewidths=0.5, linecolor="white", square=True, ax=ax)
            ax.set_title(titulo)
        Visualizacao._finalizar(fig)
