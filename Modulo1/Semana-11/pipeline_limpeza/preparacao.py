"""Preparação para modelagem: escalas (parâmetros só do treino) e divisão treino/teste."""
import numpy as np


class Escalonador:
    """Os parâmetros vêm SEMPRE do treino; o teste só é transformado."""

    @staticmethod
    def normalizar_minmax(treino, teste, colunas):
        minimo, maximo = treino[colunas].min(), treino[colunas].max()
        faixa = (maximo - minimo).replace(0, 1)
        return (treino[colunas] - minimo) / faixa, (teste[colunas] - minimo) / faixa

    @staticmethod
    def padronizar_treino_teste(treino, teste, colunas):
        media, desvio = treino[colunas].mean(), treino[colunas].std().replace(0, 1)
        return (treino[colunas] - media) / desvio, (teste[colunas] - media) / desvio


class DivisorTreinoTeste:
    def __init__(self, fracao_teste=0.2, semente=42):
        self.fracao_teste = fracao_teste
        self.semente = semente

    def dividir(self, dados):
        rng = np.random.default_rng(self.semente)
        ordem = rng.permutation(len(dados))
        n_teste = int(round(len(dados) * self.fracao_teste))
        teste = dados.iloc[ordem[:n_teste]]
        treino = dados.iloc[ordem[n_teste:]]
        return treino.reset_index(drop=True), teste.reset_index(drop=True)
