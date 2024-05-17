from .SolucaoRoad import SolucaoRoad
from typing import List

class SolucaoTrails:
    def __init__(self):
        self.patio = 0
        self.roads: List[SolucaoRoad] = []
        self.tempoTotal = 0.0
        self.distanciaTotal = 0.0
        self.FOTotal = 0.0
    
    def __str__(self):
        print("---- Solucao Trails ----")
        print("Patio: " + str(self.patio))
        print("DistanciaTotal: " + str(self.distanciaTotal))
        print("FOTotal: " + str(self.FOTotal))
        print("Roads: ")
        for road in self.roads:
            road.__str__()


class SolucaoPtTrails:

    def __init__(self) -> None:
        self.patios = [int() for _ in range(100)]
        self.volumes = [float() for _ in range(100)]
        self.distanciaTotal = 0.0
        self.FO = 0.0
        self.tempoSol = 0.0
        self.tempo = 0.0
        self.numIteracoes = 0
        self.numViaveis = 0
        self.numInviaveis = 0
        self.viavel = 0
    
    def __str__(self): 
        print("---- Solucao PtTrails ----")
        print("patios: ")
        print(self.patios)
        print("Volumes: ")
        print(self.volumes)
        print("FO: " + str(self.FO))
        print("Distancia total: " +str(self.distanciaTotal))
        print("NumIteracoes: " + str(self.numIteracoes))
        print("NumViaveis: " + str(self.numViaveis))
        print("NumInviaveis: " + str(self.numInviaveis))
        print("Viavel: " + str(self.viavel))
        print("-------------------------- \n")