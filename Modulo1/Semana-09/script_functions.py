import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

referencia = pd.Timestamp("2026-09-30")
sns.set_theme(
    style="whitegrid",
    context="notebook",
    palette="pastel" # "Set2", "muted"
)

plt.rcParams.update({
    "figure.figsize": (10, 5), "font.size": 11,
    "axes.facecolor": "#F7FAFC", "figure.facecolor": "white",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titleweight": "bold", "axes.titlesize": 14,
    "axes.titlepad": 18, "grid.alpha": 0.28,
    "grid.color": "#A6BBC7", "axes.edgecolor": "#CBD5DD"
})

print("Referência:", referencia.date())
print("Dados fictícios para uso didático.")


# funcao de mostrar dataframe
def mostrar(tabela, num_show=8):
    print(tabela.head(num_show).round(2).to_string(index=False))

# funcao de mostrar grafico de barras vertical
def barras_vertical(tabela, categoria, valor, titulo=None):
    '''
    Param:
        tabela: dataframe
        categoria: str
        valor: str
        titulo: str
    '''
    fig, ax = plt.subplots()
    sns.barplot(data=tabela, x=categoria, y=valor, hue=categoria,
                legend=False, errorbar=None,
                orient="v", width=0.72, ax=ax)
    ax.set_title(titulo)
    ax.set_xlabel(categoria.replace("_", " ").capitalize())
    ax.set_ylabel(valor.replace("_", " ").capitalize())
    ax.grid(axis="x", visible=False)
    ax.margins(y=0.18)
    ax.tick_params(axis="x", labelrotation=28)
    for grupo in ax.containers:
        ax.bar_label(grupo, fmt="%.0f", padding=4, fontsize=10)
    sns.despine(ax=ax, left=True, bottom=True) # remover bordas
    fig.tight_layout() # ajusta automaticamente os espaçoes
    plt.show()    

# funcao de mostra grafico barras horizontal
def barras_horizontal(tabela, categoria, valor, titulo=None):
    '''
    Param:
        tabela: dataframe
        categoria: str
        valor: str
        titulo: str
    '''
    fig, ax = plt.subplots()
    sns.barplot(data=tabela, x=valor, y=categoria, hue=categoria,
                legend=False, errorbar=None,
                orient="h", width=0.72, ax=ax)
    ax.set_title(titulo, loc="center")
    ax.set_xlabel(valor.replace("_", " ").capitalize())
    ax.set_ylabel(categoria.replace("_", " ").capitalize())
    ax.grid(axis="y", visible=False)
    ax.margins(x=0.2)
    for grupo in ax.containers:
        ax.bar_label(grupo, fmt="%.0f", padding=4, fontsize=10)
    sns.despine(ax=ax, left=True, bottom=True)
    fig.tight_layout()
    plt.show()

# funcao para mostra grafico de pizza com porcentagem
def pizza(tabela, rotulo, valor, titulo=None):
    '''
    Param:
        tabela: dataframe
        rotulo: str
        valor: str
        titulo: str
    '''
    fig, ax = plt.subplots()
    ax.pie(tabela[valor], labels=tabela[rotulo],
           autopct="%1.1f%%", startangle=90, pctdistance=0.7,
           wedgeprops={"edgecolor": "white", "linewidth": 2},
           textprops={"color": "#23373B", "fontsize": 12})
    ax.set_title(titulo)
    ax.axis("equal")
    fig.tight_layout()
    plt.show()

# funcao para mostra grafico de dispersão
def dispersao(tabela, x, y, titulo=None):
    '''
    Param:
        tabela: dataframe
        x: str
        y: str
        titulo: str
    '''
    fig, ax = plt.subplots()
    sns.scatterplot(data=tabela, x=x, y=y,
                    alpha=0.5, s=35, color="#2A7F87",
                    edgecolor="white", linewidth=0.35, ax=ax)
    ax.set_title(titulo)#.replace("_", " "))
    ax.set_ylabel(y)#.replace("_", " "))
    ax.set_xlabel(x)#.replace("_", " "))
    sns.despine(ax=ax)
    fig.tight_layout()
    plt.show()

# funcao para mostra grafico de linhas
def linhas(tabela, x, y, mark='o', titulo=None):    
    '''
    Param:
    tabela: dataframe
    x: str
    y: str
    titulo: str
    '''
    fig, ax = plt.subplots()
    sns.lineplot(data=tabela, x=x, y=y,
                 marker=mark, markersize=7, linewidth=1.8,
                 color="#2A7F87", ax=ax)
    ax.set_title(titulo)
    sns.despine(ax=ax)
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.show()