from .commons import calculaDistancia
from .QuickSort import quickSort
from ..Models.Patio import Patio
from ..Models.SolucaoStorageYard import SolucaoStorageYard

class PreProcecamentoRoads:
    def __init__(self, NUM_PATIOS, patios, solPatios):
        self.distanciaPatios = [[0.0 for _ in range(NUM_PATIOS)] for _ in range(NUM_PATIOS)]
        self.patiosOrder = [[-1 for _ in range(NUM_PATIOS)] for _ in range(NUM_PATIOS)]
        self.vPatiosSecOrder = [[-1 for _ in range(NUM_PATIOS)] for _ in range(NUM_PATIOS)]
        self.verticesSecP = [0 for _ in range(NUM_PATIOS)]
        self.patiosP = [0 for _ in range(NUM_PATIOS)]

        self.calculaDistanciaSolPatios(patios, solPatios, self.distanciaPatios, self.patiosP, self.verticesSecP, NUM_PATIOS)
        self.ordenaDistanciaPatioPatios(self.distanciaPatios, self.patiosOrder, self.vPatiosSecOrder, self.patiosP, self.verticesSecP, NUM_PATIOS)

    def calculaDistanciaSolPatios(self, patios: list[Patio], solPatios: SolucaoStorageYard, distanciasPatios: list[list[float]], idPatios: list[int], vertices: list[int], NUM_PATIOS):
        distancia3d = 0.0
        
        for i in range(NUM_PATIOS):
            patI = patios[solPatios.patios[i] - 1]
            for j in range(i, NUM_PATIOS):
                patJ = patios[solPatios.patios[j] - 1]
                distancia3d = calculaDistancia(patI,patJ)
                distanciasPatios[i][j] = distancia3d
                distanciasPatios[j][i] = distancia3d
            idPatios[i] = solPatios.patios[i]
            vertices[i] = patI.vertice - 1

    def ordenaDistanciaPatioPatios(self, distanciaPatios, patiosOrder, vPatiosOrder, idPatios, vertices, NUM_PATIOS):
        distanciaOrder = [0.0 for _ in range(NUM_PATIOS)]
        for i in range(NUM_PATIOS):
            #carregando os patios do patio
            for j in range(NUM_PATIOS):
                distanciaOrder[j] = distanciaPatios[i][j]
                patiosOrder[i][j] = idPatios[j]
                vPatiosOrder[i][j] = vertices[j]
            #ordena os patios do patio 
            quickSort(distanciaOrder, patiosOrder[i], vPatiosOrder[i], 0, NUM_PATIOS -1)
            #ordenando a matriz de distancias
            for j in range(NUM_PATIOS):
                distanciaPatios[i][j] = distanciaOrder[j]
