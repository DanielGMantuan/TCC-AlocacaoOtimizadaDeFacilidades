from math import sqrt, pow, inf as INFINITY
from ..Models.Area import Area
from ..Models.ArvoreExploravel import ArvoreExploravel
from ..Models.Patio import Patio
from typing import List
from ..Models.SolucaoStorageYard import SolucaoStorageYard
from ..Models.Desvio import Desvio
from ..Models.Inclinacao import Inclinacao

#--------------------------------- CONSTANTS --------------------------------#
PENALIZACAO_APP = 4
PENALIZACAO_INUND = 2
PENALIZACAO_INCL_8 = 1
PENALIZACAO_INCL_10 = 2
PENALIZACAO_INCL_100 = 2
PENALIZACAO_OBSTACULO = 2

NUM_DESVIOS = 559
AVOID_RADIUS = 15
#---------------------------------- DISTANCIAS -------------------------------#
def calculaDistancia(origem, destino):
    distancia = sqrt(pow(origem.x - destino.x, 2) + pow(origem.y - destino.y, 2) + pow(origem.z - destino.z, 2))
    return distancia

def calculaDistancia2D(origem, destino):
    distancia = sqrt(pow(origem.x - destino.x, 2) + pow(origem.y - destino.y, 2))
    return distancia

def calculaDistanciaPenalizada(distanciaOrigDest: float, destino: Area, desvios: list[Desvio], app: list[int], inund: list[int], inclinacao: list[Inclinacao]) -> float:
    indApp = buscaAPP(app, (destino.id - 1))
    indInund = buscaInund(inund, (destino.id - 1))
    indObstaculo = buscaDesvioRaio(desvios, destino)
    if(indObstaculo):
        distanciaOrigDest = distanciaOrigDest * PENALIZACAO_OBSTACULO
    if(indApp):
        distanciaOrigDest = distanciaOrigDest * PENALIZACAO_APP
    if(indInund):
        distanciaOrigDest = distanciaOrigDest * PENALIZACAO_INUND
    distanciaOrigDest = distanciaOrigDest * buscaInclinacao(inclinacao, (destino.id - 1))
    return distanciaOrigDest

def calculaDistanciaDesviosPenalizada(origem, destino, desvios: list[Desvio]) -> float:
    indObstaculo = buscaDesvioRaio(desvios, destino)
    distancia = calculaDistancia(origem, destino)
    if(indObstaculo):
        distancia *= PENALIZACAO_OBSTACULO

    return distancia

#---------------------------------- PENALIZACAO --------------------------------#
def buscaAPP(vetVerticesApp: list[int], destino: int):
    if destino in vetVerticesApp:
        return 1
    return 0

def buscaInund(vetVerticesInund: list[int], destino: int):
    if destino in  vetVerticesInund:
        return 1
    return 0

def buscaInclinacao(vetInclinacao: list[Inclinacao], destino:int):
    i = vetInclinacao[destino]
    
    if i == 1:
        return PENALIZACAO_INCL_8
    elif i == 2:
        return PENALIZACAO_INCL_10
    elif i == 3:
        return PENALIZACAO_INCL_100
    else:
        return PENALIZACAO_INCL_8

#------------------------------------- Buscas -------------------------#
def buscapatio(patio, vetVertices):
    for vertice in vetVertices:
        if (patio[0] == vertice[0]) and (patio[1] == vertice[1]):
            return vetVertices.index(vertice)
    return -1

def buscaPatioInLayer(patio: Patio, area: list[Area]):
    for vertice in area:
        if (patio.x == vertice.x) and (patio.y == vertice.y):
            return vertice.id
    return -1

def buscaDesvioRaio(desvios: list[Desvio], destino):
    for i in range(NUM_DESVIOS):
        distancia = sqrt(pow(desvios[i].x - destino.x, 2) + pow(desvios[i].y - destino.y, 2) + pow(desvios[i].z - destino.z, 2))
        if distancia <= AVOID_RADIUS:
            return desvios[i].id
    return 0
# ----------------------------------------------------------------------------#
def marcaArvoresPatios(sol: SolucaoStorageYard, matriz: List[List[float]], NUM_ARVORES_EXPLORAVEIS, NUM_PATIOS) -> List[List[int]]: 
    #zerando arvores selecionadas
    arvoreSelPatios = [[0 for _ in range(NUM_ARVORES_EXPLORAVEIS)] for _ in range(NUM_PATIOS)]

    #comparando as distancias dos pontos aleatorios para marcar as arvores
    for j in range(NUM_ARVORES_EXPLORAVEIS):
        distanciaMenor = INFINITY
        patio: int = 0
        for k in range(NUM_PATIOS):
            distancia = matriz[j][sol.patios[k]-1]
            if distancia < distanciaMenor:
                distanciaMenor = distancia
                patio = k
        arvoreSelPatios[patio][j] = 1
    
    return arvoreSelPatios

def quantidadeArvoresPatio(arvoreSelPatios: List[List[int]], NUM_PATIOS, NUM_ARVORES_EXPLORAVEIS) -> List[int]:
    quantidadeArvores = [0 for _ in range(NUM_PATIOS)]
    
    for i in range(NUM_PATIOS):
        for j in range(NUM_ARVORES_EXPLORAVEIS):
            if arvoreSelPatios[i][j]==1:
                quantidadeArvores[i] = quantidadeArvores[i] + 1
    print("vetor quantidadeArvoresn\n[")
    print(quantidadeArvores)
    return quantidadeArvores
        


#def buscaAPP(APP, vertice):
#    return APP[vertice]

#def buscaInund(Inund, vertice):
#    return Inund[vertice]