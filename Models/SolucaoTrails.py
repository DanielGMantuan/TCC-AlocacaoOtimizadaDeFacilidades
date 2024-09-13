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
        
        result = "---- Solucao Trails ----" + "\n"
        result += "Patio: " + str(self.patio) + "\n"
        result += "DistanciaTotal: " + str(self.distanciaTotal) + "\n"
        result += "FOTotal: " + str(self.FOTotal) + "\n"
        result += "Roads: " + "\n"
        for road in self.roads:
            result += road.__str__() + "\n"
        
        return result

    def fileWritter(self, index: int, path: str):
        caminho = fr"{path}\trilhas\patio{self.patio}.txt"

        with open(caminho, "w") as arquivo:
            arquivo.write("---- Solucao Trails ----" + "\n")
            arquivo.write("Patio: " + str(self.patio) + "\n")
            arquivo.write("DistanciaTotal: " + str(self.distanciaTotal) + "\n")
            arquivo.write("FOTotal: " + str(self.FOTotal) + "\n")
            arquivo.write("Roads: " + "\n")
            for road in self.roads:
                arquivo.write(road.__str__() + "\n")

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
        result = "---- Solucao PtTrails ----" + "\n"
        result += "patios: " + "\n"
        result += str(self.patios) + "\n"
        result += "Volumes: " + "\n"
        result += str(self.volumes) + "\n"
        result += "FO: " + str(self.FO) + "\n"
        result += "Distancia total: " +str(self.distanciaTotal) + "\n"
        result += "NumIteracoes: " + str(self.numIteracoes) + "\n"
        result += "NumViaveis: " + str(self.numViaveis) + "\n"
        result += "NumInviaveis: " + str(self.numInviaveis) + "\n"
        result += "Viavel: " + str(self.viavel) + "\n"
        result += "-------------------------- \n" + "\n"
