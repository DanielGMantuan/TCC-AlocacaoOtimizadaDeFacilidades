from .Models.SolucaoStorageYard import SolucaoStorageYard
from .Models.ArvoreExploravel import ArvoreExploravel
from .Heuristicas import Heuristicas
from datetime import datetime
from random import seed, randint
import time
import math
import copy

class SA:

    def __init__(self, NUM_PATIOS: int, NUM_ARVORES_EXPLORAVEIS: int, DISTANCIA_MAXIMA: float, NUM_VERTICES_PATIOS: int, PENALIZACAO_VOLUME: int, TEMPOEXEC: int):
        self.NUM_PATIOS = NUM_PATIOS
        self.NUM_ARVORES_EXPLORAVEIS = NUM_ARVORES_EXPLORAVEIS
        self.DISTANCIA_MAXIMA = DISTANCIA_MAXIMA
        self.NUM_VERTICES_PATIOS = NUM_VERTICES_PATIOS
        self.PENALIZACAO_VOLUME = PENALIZACAO_VOLUME
        self.TEMPOEXEC = TEMPOEXEC

    def gerarVizinhoPatio(self, floresta: list[ArvoreExploravel], distancias: list[list[float]], sol: SolucaoStorageYard, patios: list[int], restVolSup: float):
        solAtual = copy.deepcopy(sol)
        vizinho = 0

        # obtendo a posicao aleatoria de troca
        # troca = randint(1, 32767) % NUM_PATIOS
        troca = randint(1, self.NUM_PATIOS) - 1

        while True:
            # vizinho = 1 + (randint(1, 32767) % NUM_VERTICES_PATIOS)
            vizinho = randint(1, self.NUM_VERTICES_PATIOS)
            if patios[vizinho - 1] != 1:
                solAtual.patios[troca] = vizinho
                break

        # depois de selecionar um número, marca ele como já tendo sido selecionado
        patios[vizinho - 1] = 1

        heuristica = Heuristicas(self.NUM_PATIOS, self.NUM_ARVORES_EXPLORAVEIS, self.DISTANCIA_MAXIMA, self.NUM_VERTICES_PATIOS, self.PENALIZACAO_VOLUME)
        # atualiza árvores alocadas e calcula FO ----------- falta implementar essa parte do java
        solAtual = heuristica.calculaFOPatio(floresta, distancias, solAtual, restVolSup)

        return solAtual

    def SAStorageYard(self, floresta: list[ArvoreExploravel], distancias: list[list[float]], solInicial: SolucaoStorageYard, restVolSup: float, txResfriamento: float, iteracoesVizinhanca: float, tempInicial: float, tempCongelamento: float) -> SolucaoStorageYard:
        # inicializando variáveis
        tfInicio = datetime.now() # get_time
        i = 0
        j = 0
        k = 0
        patio = 0
        cont = 0
        contViaveis = 0
        contInviaveis = 0
        tInicio = time.time() # inicializando o tempo atual
        # tFim = tInicio + (TEMPOEXEC * CLOCKS_PER_SEC) # determinando o tempo de duração do laço externo
        tFim = tInicio + self.TEMPOEXEC

        melhorSol = copy.deepcopy(solInicial)
        solucaoInicial = copy.deepcopy(solInicial)
        vizinho = SolucaoStorageYard()
        melhorSol.numViaveis = 0
        melhorSol.numInviaveis = 0
        patios = [0 for _ in range(self.NUM_VERTICES_PATIOS)]

        # marcando com 1 os elementos da solução inicial
        for k in range(self.NUM_PATIOS):
            patio = solucaoInicial.patios[k]
            patios[patio - 1] = 1

        # inicializando variáveis
        IterTemp = 0                   # numero de iterações na temperatura T
        temp = tempInicial             # temperatura corrente
        x = 0.0
        variacao = 0.0

        while temp > tempCongelamento and time.time() < tFim:
            while IterTemp < iteracoesVizinhanca and time.time() < tFim:
                IterTemp = IterTemp + 1
                cont = cont + 1
                vizinho = self.gerarVizinhoPatio(floresta, distancias, solucaoInicial, patios, restVolSup)
                # obtendo a variação da solução inicial para o vizinho
                variacao = vizinho.FO - solucaoInicial.FO
                # print("Melhor:"+ str(melhorSol.FO) +" vizinho.FO:" + str(vizinho.FO) + " solucaoInicial.FO:" + str(solucaoInicial.FO) + " variacao:" + str(variacao))
                if vizinho.viavel == True:
                    contViaveis = contViaveis + 1
                else:
                    contInviaveis = contInviaveis + 1

                patios = [0 for _ in range(self.NUM_VERTICES_PATIOS)]

                # se a variação é menor q zero, então melhorou
                if variacao < 0:
                    # print("melhor.FO:" + str(melhorSol.FO))
                    # melhorou a solução inicial em relação ao vizinho
                    solucaoInicial = vizinho
                    for i in range(self.NUM_PATIOS):
                        patio = vizinho.patios[i]
                        patios[patio - 1] = 1

                    if vizinho.FO < melhorSol.FO:
                        # melhorou a melhor até o momento em relação ao vizinho
                        melhorSol = vizinho
                        melhorSol.tempoSol = (datetime.now() - tfInicio).total_seconds() # get_time
                else:
                    # x = (randint(1, 32767) % 1001)
                    x = randint(0, 1000)
                    x = x / 1000
                    if x < math.pow(math.e, (-variacao / temp)):
                        # atualizando matriz da solução atual
                        # pega o vizinho mesmo este não sendo melhor
                        solucaoInicial = vizinho
                        # print("pegando mesmo estando ruim")
                        for i in range(self.NUM_PATIOS):
                            patio = vizinho.patios[i]
                            patios[patio - 1] = 1
                    else:
                        # print("corrigindo")
                        # corrige solução atual
                        for j in range(self.NUM_PATIOS):
                            patio = solucaoInicial.patios[j]
                            patios[patio - 1] = 1
                
            temp = txResfriamento * temp

            # re-annealing
            if temp < (tempCongelamento + (tempCongelamento * 2)) and time.time() < tFim:
                temp = tempInicial

            IterTemp = 0

        melhorSol.tempo = (datetime.now() - tfInicio).total_seconds()
        melhorSol.numIteracoes = cont
        melhorSol.numViaveis = contViaveis
        melhorSol.numInviaveis = contInviaveis
        return melhorSol

