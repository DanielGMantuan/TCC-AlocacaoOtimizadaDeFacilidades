from .Models.SolucaoStorageYard import SolucaoStorageYard
from .Models.ArvoreExploravel import ArvoreExploravel
from datetime import datetime
from random import seed, randint
import math
import copy

class Heuristicas:

    def __init__(self, NUM_PATIOS, NUM_ARVORES_EXPLORAVEIS, DISTANCIA_MAXIMA, NUM_VERTICES_PATIOS, PENALIZACAO_VOLUME):
        self.NUM_PATIOS = NUM_PATIOS
        self.NUM_ARVORES_EXPLORAVEIS = NUM_ARVORES_EXPLORAVEIS
        self.DISTANCIA_MAXIMA = DISTANCIA_MAXIMA
        self.NUM_VERTICES_PATIOS = NUM_VERTICES_PATIOS
        self.PENALIZACAO_VOLUME = PENALIZACAO_VOLUME

    def calculaFOPatio(self, floresta: list[ArvoreExploravel], distancias: list[list[float]], solAtual: SolucaoStorageYard, restVolSup: float) -> SolucaoStorageYard:
        patio = 0
        distancia = 0
        distanciaMenor = 0
        diferencaVolume = 0 
        diferencaDistancia = 0
        distanciaTotal = 0
        res = copy.deepcopy(solAtual)

        res.volumes = [0 for _ in range(self.NUM_PATIOS)]
        res.arvores = [[] for _ in range(14)]   

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
        return res

    def obterSolAleatoria(self, floresta: list[ArvoreExploravel], distancias: list[list[float]], restVolSup: float) -> SolucaoStorageYard:
        patio = 0
        patios = [0 for _ in range(self.NUM_VERTICES_PATIOS)]  # vetor que vai guardar a informação dos patios que já foram selecionados

        res = SolucaoStorageYard()
        res.patios = [0 for _ in range(self.NUM_PATIOS)]
        res.volumes = [0 for _ in range(self.NUM_PATIOS)]

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
        return res

    def heuConstrutivaIter(self, floresta: list[ArvoreExploravel], distancias: list[list[float]], num_iteracoes: int, restVolSup: float) -> SolucaoStorageYard:
        tInicio = datetime.now()
        i = 0
        cont = 0
        contViaveis = 0
        melhorSol = SolucaoStorageYard()
        res = SolucaoStorageYard()
        melhorSol.FO = math.inf  # variaveis para controle da FO
        melhorSol.numViaveis = 0
        melhorSol.numInviaveis = 0

        # laço que faz a busca aleatório e gulosa
        for i in range(num_iteracoes):
            cont = cont + 1
            res = self.obterSolAleatoria(floresta, distancias, restVolSup)

            # print(res.FO)
            # print(melhorSol.FO)
            if res.FO < melhorSol.FO: # se a FO atual é melhor que a anterior e viável, então aceita a atual
                melhorSol = res
                # print(melhorSol.FO)
                melhorSol.tempoSol = (datetime.now() - tInicio).total_seconds()

            if res.viavel:
                contViaveis = contViaveis + 1
            
        melhorSol.tempo = (datetime.now() - tInicio).total_seconds()
        melhorSol.numIteracoes = cont
        melhorSol.numViaveis = contViaveis
        melhorSol.numInviaveis = cont - contViaveis

        return melhorSol

    

