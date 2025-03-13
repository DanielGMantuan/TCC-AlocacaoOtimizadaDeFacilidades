from .Models.SolucaoStorageYard import SolucaoStorageYard
from .Models.ArvoreExploravel import ArvoreExploravel
from random import seed, randint
import math
import time
import copy
import gc
from alocacao_otimizada import TadRoadForest

class Heuristicas:

    def __init__(self, NUM_PATIOS: int, NUM_ARVORES_EXPLORAVEIS: int, DISTANCIA_MAXIMA: float, NUM_VERTICES_PATIOS: int, PENALIZACAO_VOLUME: int):
        self.NUM_PATIOS = NUM_PATIOS
        self.NUM_ARVORES_EXPLORAVEIS = NUM_ARVORES_EXPLORAVEIS
        self.DISTANCIA_MAXIMA = DISTANCIA_MAXIMA
        self.NUM_VERTICES_PATIOS = NUM_VERTICES_PATIOS
        self.PENALIZACAO_VOLUME = PENALIZACAO_VOLUME


    def calculaFOPatio(self, floresta: list[ArvoreExploravel], distancias: list[list[float]], solAtual: SolucaoStorageYard, restVolSup: float) -> SolucaoStorageYard:
        tInicio = time.time()
        patio = 0
        distancia = 0
        distanciaMenor = 0
        diferencaVolume = 0 
        diferencaDistancia = 0
        distanciaTotal = 0
        res = copy.deepcopy(solAtual)
        res.t = 0.0

        res.volumes = [0 for _ in range(self.NUM_PATIOS)]
        res.arvores = [[] for _ in range(self.NUM_PATIOS)]   

        #Comparando as distancias dos pontos aleatorios
        for j in range(self.NUM_ARVORES_EXPLORAVEIS):
            distanciaMenor = math.inf
            patio = 0
            for k in range(self.NUM_PATIOS):
                distancia = distancias[j][res.patios[k] - 1]
                if distancia < distanciaMenor:
                    distanciaMenor = distancia
                    patio = k

            if distanciaMenor > self.DISTANCIA_MAXIMA:
                diferencaDistancia += distanciaMenor - self.DISTANCIA_MAXIMA
            distanciaTotal += distanciaMenor

            nova_arvore = {'id': floresta[j].id, 'numero': floresta[j].numero}
            res.arvores[patio].append(nova_arvore)
            res.volumes[patio] += floresta[j].volume

        for w in range(self.NUM_PATIOS):
            diferencaVolume += (res.volumes[w] - restVolSup) if (res.volumes[w] > restVolSup) else 0
            
        res.distanciaTotal = distanciaTotal
        #penalizar solucao inviavel
        distanciaTotal +=  self.PENALIZACAO_VOLUME * (diferencaVolume + diferencaDistancia) # penalizacao é o theta e diferença é g()

        res.FO = distanciaTotal
        res.viavel = (diferencaVolume + diferencaDistancia) == 0

        res.t = time.time() - tInicio
        return res

    def obterSolAleatoria(self, floresta: list[ArvoreExploravel], distancias: list[list[float]], restVolSup: float) -> SolucaoStorageYard:
        patio = 0
        patios = [0 for _ in range(self.NUM_VERTICES_PATIOS)]  # vetor que vai guardar a informação dos patios que já foram selecionados

        res = SolucaoStorageYard()
        res.patios = [0 for _ in range(self.NUM_PATIOS)]
        res.volumes = [0.0 for _ in range(self.NUM_PATIOS)]

        # gera os números aleatórios de acordo com o número de pátios
        for i in range(self.NUM_PATIOS):
            # garante que será gerado um número aleatório sem repetição
            while True:  
                # patio = 1 + (randint(1, 32767) % NUM_VERTICES_PATIOS) # 32767 = RAND_MAX no C
                patio = randint(1, self.NUM_VERTICES_PATIOS)
                if patios[patio - 1] != 1:  
                    break
            # depois de selecionar um número, marca ele como já tendo sido selecionado e atribui ao pátio        
            patios[patio - 1] = 1
            res.patios[i] = patio

        res = self.calculaFOPatio(floresta, distancias, res, restVolSup)
        # TadRoadForest.calculaFOPatio(res, restVolSup)
        # res = SolucaoStorageYard.from_dict(res2dict)
        # print(f"Patios: {res.patios.__len__()}")
        # print(f"Patios: {res.patios}")
        # print(f"Volumes: {res.volumes}")
        # print(f"Distancia Total: {res.distanciaTotal}")
        # print(f"FO: {res.FO}")
        # print(f"Tempo Solução: {res.tempoSol}")
        # print(f"Tempo: {res.tempo}")
        # print(f"Num Iterações: {res.numIteracoes}")
        # print(f"Num Viáveis: {res.numViaveis}")
        # print(f"Num Inváveis: {res.numInviaveis}")
        # print(f"Viável: {res.viavel}")
        # print(f"Arvores: {res.arvores.__len__()}")
        # print(f"Arvores: {res.arvores}")
        # print(f"Tempo Cálculo FO Total: {res.tempoCalculoFO_Total}")
        # print(f"Tempo Cálculo FO SA: {res.tempoCalculoFO_SA}")
        # print(f"Tempo Cálculo FO Heurística: {res.tempoCalculoFO_Heuristica}")
        # print(f"Tempo SA: {res.tempoSA}")
        # print(f"Tempo Heurística: {res.tempoHeuristica}")
        # print(f"Tempo Total: {res.tempoTotal}")
        # print(f"T: {res.t}")
        # print(f"Tempo Djikstra: {res.tempoDjisktra}")
        # print(f"Qgis FO: {res.FO}")
        # print(f"Num patios: {self.NUM_PATIOS}")
        # print(type(res2), res2)
        # print(res.arvores)
        # print(res2.arvores)
        
        # del res2dict
        # gc.collect()

        return res

    def heuConstrutivaIter(self, floresta: list[ArvoreExploravel], distancias: list[list[float]], num_iteracoes: int, restVolSup: float) -> SolucaoStorageYard:
        tInicio = time.time()
        i = 0
        cont = 0
        contViaveis = 0
        melhorSol = SolucaoStorageYard()
        res = SolucaoStorageYard()
        melhorSol.FO = math.inf  # variaveis para controle da FO
        melhorSol.numViaveis = 0
        melhorSol.numInviaveis = 0
        tempoCalculoFOHeuristica = 0.0

        # laço que faz a busca aleatório e gulosa
        for i in range(num_iteracoes):
            cont = cont + 1
            res = self.obterSolAleatoria(floresta, distancias, restVolSup)
            tempoCalculoFOHeuristica += res.t

            if res.FO < melhorSol.FO: # se a FO atual é melhor que a anterior e viável, então aceita a atual
                melhorSol = res
                melhorSol.tempoSol = time.time() - tInicio

            if res.viavel:
                contViaveis = contViaveis + 1
            
        melhorSol.tempo = time.time() - tInicio
        melhorSol.tempoHeuristica = melhorSol.tempo
        melhorSol.numIteracoes = cont
        melhorSol.numViaveis = contViaveis
        melhorSol.numInviaveis = cont - contViaveis
        melhorSol.tempoCalculoFO_Heuristica = tempoCalculoFOHeuristica

        return melhorSol