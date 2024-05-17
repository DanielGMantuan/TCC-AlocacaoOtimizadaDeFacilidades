from Models.SolucaoRoad import Road, SolucaoPrimaryRoad, SolucaoRoad, AccessRoad
from .Models.Grafo import Grafo

def primaryRoad(grafo, pPrimaryRoad):
    sol = SolucaoRoad()
    solAux = SolucaoRoad()
    solucaoPrimaryRoad = SolucaoPrimaryRoad()
    solucaoPrimaryRoad.numTotalVerticesRota = 0
    solucaoPrimaryRoad.FO_Total = 0
    solucaoPrimaryRoad.distanciaTotal = 0

    for i in range(1): #range tem referencia no numero de entradas diferentes
        if i == 0:
            #primeiro trecho de estrada primaria
            p = pPrimaryRoad.inicio
            t = pPrimaryRoad.termino
            sol = grafo.Dijkstra(p, t)
        #else:
            #n-esimo trecho de estrada primaria
            #TODO: ainda nao e necessario
        solucaoPrimaryRoad.roads[i] = sol
        solucaoPrimaryRoad.numTotalVerticesRota += sol.numVericesRota
        solucaoPrimaryRoad.FO_Total += sol.FO
        solucaoPrimaryRoad.distanciaTotal += sol.distaciaTotal
    print(solucaoPrimaryRoad)