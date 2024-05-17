class Road:
    def __init__(self):
        self.inicio = 0
        self.termino = 0

class AccessRoad:
    def __init__(self):
        self.inicio : list[int] = []
        self.termino = 0

class SolucaoRoad:
    def __init__(self, NUM_VERTICES):
        self.estrada = Road()
        self.FO = 0.0
        self.distanciaTotal = 0.0
        self.numVerticesRota = 0
        self.antecessor = [-1 for _ in range(NUM_VERTICES)]
        self.sucessor = [-1 for _ in range(NUM_VERTICES)]
        self.distancia = [-1.0 for _ in range(NUM_VERTICES)]
        self.peso = [-1.0 for _ in range(NUM_VERTICES)]
        self.tempoSol = 0.0
        self.tempo = 0.0
        self.cicloNegativo = 0
        self.verticesRoad = []
    
    def __str__(self):
        result = "\n----Solucao Road"
        result += "\ninicio:" + str(self.estrada.inicio)
        result += "\ntermino:" + str(self.estrada.termino)
        result += "\ndistancia total:" + str(self.distanciaTotal)
        result += "\nnumero de vertices na rota:" + str(self.numVerticesRota)
        result += "\n Vertices da rota: \n"
        for vertice in self.verticesRoad:
            result += str(vertice) +','
        result += "\n"

        print(result)
        #print("pesos")
        #print(self.peso)
        #print("antecessor:")
        #print(self.antecessor)
        #print("sucessor:")
        #print(self.sucessor)

class SolucaoPrimaryRoad:
    def __init__(self, NUM_PRIMARY_ROAD, NUM_VERTICES):
        self.roads = [SolucaoRoad(NUM_VERTICES) for _ in range(NUM_PRIMARY_ROAD)]
        self.numTotalVerticesRota = 0
        self.tempoTotal = 0.0
        self.distanciaTotal = 0.0
        self.FO_Total = 0.0

class SolucaoSecondaryRoad:
    def __init__(self, NUM_PATIOS, NUM_VERTICES):
        self.roads = [SolucaoRoad(NUM_VERTICES) for _ in range(NUM_PATIOS)]
        self.tempoTotal = 0.0
        self.distanciaTOtal = 0.0
        self.FOTotal = 0.0

class SolucaoRoads:
    def __init__(self, NUM_ROADS, NUM_VERTICES):
        self.roads = [SolucaoRoad(NUM_VERTICES) for _ in range(NUM_ROADS)]
        self.typeRoad = [0 for _ in range(NUM_ROADS)]
        self.tempoTotal = 0.0
        self.distanciaTotal = 0.0
        self.FOTotal = 0.0
        
    def __str__(self):
        for road in self.roads:
            print("roads", end=" ")
            print(self.typeRoad[self.roads.index(road)])
            road.__str__()
        print("typeroads")
        print(self.typeRoad)
        print("tempo total\n" + str(self.tempoTotal))
        print("distancia total\n" + str(self.distanciaTotal))
        print("FOTotal\n" + str(self.FOTotal))