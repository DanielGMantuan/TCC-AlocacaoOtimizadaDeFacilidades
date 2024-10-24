from typing import Optional
from .SolucaoRoad import SolucaoRoad 
from ..Services.commons import calculaDistancia,calculaDistanciaPenalizada, calculaDistancia2D, calculaDistanciaDesviosPenalizada
from .Area import Area
from .Desvio import Desvio
from .Inclinacao import Inclinacao
import time

NUM_DIS_MAX_VIZINHO = int(43)

class Grafo:
    def __str__(self):
        string = "----GRAFO---- \n"
        string += "numero de vertices:" + str(self.nro_vertices) + "\n"
        string += "Ponderado:" + str(self.eh_ponderado) + "\n"
        string += "grau de cada vertice:" + "\n"
        string += str(self.grau) + "\n"
        string += "distancia em cada vertice:" + "\n"
        string += str(self.distancia) + "\n"
        string += "arestas:" + "\n"
        string += str(self.arestas) + "\n"
        string += "matriz de pesos:" + "\n"
        string += str(self.pesos) + "\n"

        return string

    def cria_Grafo(self, NUM_VERTICES, grau_max, eh_ponderado):
        self.nro_vertices = NUM_VERTICES
        self.grau_max = grau_max
        self.eh_ponderado = 1 if (eh_ponderado != 0) else 0
        self.grau = [0 for _ in range(self.nro_vertices)]
        
        #Matriz de arestas
        self.arestas = [[-1 for _ in range(grau_max)] for _ in range(self.nro_vertices)]
        #Matriz de pesos
        if self.eh_ponderado:
            #Penalizacao
            self.distancia = [[0.0 for _ in range(grau_max)] for _ in range(self.nro_vertices)]
            self.pesos = [[0.0 for _ in range(grau_max)] for _ in range(self.nro_vertices)]
    
    def geraMatriz(self, area: list[Area]) -> list[list[Area]]:
        matriz: list[list[Area]] = []
        linha: list[Area] = []
        anterior = Area()
        for vertice in area:
            if anterior.id != -1 and vertice.y != anterior.y:
                matriz.append(linha)
                linha = []
            anterior = vertice
            linha.append(vertice)
        matriz.append(linha)
        
        return matriz

    def insereAresta(self, orig: int, dest: int, distancia: float, peso: float):

        #Verifica se o vertice existe
        if orig <0 or orig >= self.nro_vertices:
            return 
        
        if dest <0 or dest >= self.nro_vertices:
            return 

        #insere no final da linha do vertice de origem
        self.arestas[orig][self.grau[orig]] = dest
        if self.eh_ponderado:
            self.distancia[orig][self.grau[orig]] = distancia
            self.pesos[orig][self.grau[orig]] = peso
        self.grau[orig] = self.grau[orig] + 1
    
    def insereArestasPatios(self, area : list[Area], vertPatios: list[int], qtdPatios: int, desvios: Optional[list[Desvio]]):
        for i in range(qtdPatios):
            pOrigem = area[vertPatios[i] - 1]

            for j in range(qtdPatios):
                pDestino = area[vertPatios[j] - 1]
                distancia = calculaDistancia2D(pOrigem, pDestino)

                #TODO: verificar se esta respeitando o NUM_DIS_MAX_VIZINHO
                if distancia > 0 and distancia <= NUM_DIS_MAX_VIZINHO:
                    distancia3d = calculaDistancia(pOrigem, pDestino)
                    distanciaPenalizada = calculaDistanciaDesviosPenalizada(pOrigem, pDestino, desvios)

                    #insere aresta
                    self.insereAresta(i, j, distancia3d, distanciaPenalizada)

    def insereArestaArea(self, area: list[Area], desvios: Optional[list[Desvio]], vetInundacao: Optional[list[int]], vetApp: Optional[list[int]], vetInclinacao: list[Inclinacao]):
        matrizVertices = self.geraMatriz(area)

        MAX_LINE_SIZE = len(matrizVertices)
        MAX_COLUMN_SIZE_ANT = -1

        for line in range(MAX_LINE_SIZE): 
            MAX_COLUMN_SIZE = len(matrizVertices[line])

            if line + 1 < MAX_LINE_SIZE:
                MAX_COLUMN_SIZE_NEXT = len(matrizVertices[line+1])
            else:
                MAX_COLUMN_SIZE_NEXT = -1
            
            column = 0
            while column < MAX_COLUMN_SIZE:
                origem = matrizVertices[line][column]
                indexOrigem = origem.id - 1

                #1 vizinho
                if (line - 1) >= 0 and column < MAX_COLUMN_SIZE_ANT:
                    distancia3d = calculaDistancia(origem, matrizVertices[line - 1][column])
                    distanciaPen = calculaDistanciaPenalizada(distancia3d, matrizVertices[line - 1][column], desvios, vetApp, vetInundacao, vetInclinacao)
                    self.insereAresta(indexOrigem, matrizVertices[line - 1][column].id - 1, distancia3d, distanciaPen)
                #2 vizinho
                if (line + 1) < MAX_LINE_SIZE and column < MAX_COLUMN_SIZE_NEXT:
                    distancia3d = calculaDistancia(origem, matrizVertices[line + 1][column])
                    distanciaPen = calculaDistanciaPenalizada(distancia3d, matrizVertices[line + 1][column], desvios, vetApp, vetInundacao, vetInclinacao)
                    self.insereAresta(indexOrigem, matrizVertices[line + 1][column].id - 1, distancia3d, distanciaPen)
                #3 vizinho
                if (column - 1) >= 0:
                    distancia3d = calculaDistancia(origem, matrizVertices[line][column - 1])
                    distanciaPen = calculaDistanciaPenalizada(distancia3d, matrizVertices[line][column - 1], desvios, vetApp, vetInundacao, vetInclinacao)
                    self.insereAresta(indexOrigem, matrizVertices[line][column - 1].id - 1, distancia3d, distanciaPen)
                #4 vizinho
                if (column + 1) < MAX_COLUMN_SIZE:
                    distancia3d = calculaDistancia(origem, matrizVertices[line][column + 1])
                    distanciaPen = calculaDistanciaPenalizada(distancia3d, matrizVertices[line][column + 1], desvios, vetApp, vetInundacao, vetInclinacao)
                    self.insereAresta(indexOrigem, matrizVertices[line][column + 1].id - 1, distancia3d, distanciaPen)
                #5 vizinho
                if (line - 1) >= 0 and (column - 1) >= 0 and (column - 1) < MAX_COLUMN_SIZE_ANT :
                    distancia3d = calculaDistancia(origem, matrizVertices[line - 1][column - 1])
                    distanciaPen = calculaDistanciaPenalizada(distancia3d, matrizVertices[line - 1][column - 1], desvios, vetApp, vetInundacao, vetInclinacao)
                    self.insereAresta(indexOrigem, matrizVertices[line - 1][column - 1].id - 1, distancia3d, distanciaPen)
                #6 vizinho
                if (line + 1) < MAX_LINE_SIZE and (column - 1) >= 0 and (column - 1) < MAX_COLUMN_SIZE_NEXT:
                    distancia3d = calculaDistancia(origem, matrizVertices[line + 1][column - 1])
                    distanciaPen = calculaDistanciaPenalizada(distancia3d, matrizVertices[line + 1][column - 1], desvios, vetApp, vetInundacao, vetInclinacao)
                    self.insereAresta(indexOrigem, matrizVertices[line + 1][column - 1].id - 1, distancia3d, distanciaPen)
                #7 vizinho
                if (line - 1) >= 0 and (column + 1) < MAX_COLUMN_SIZE_ANT:
                    distancia3d = calculaDistancia(origem, matrizVertices[line - 1][column + 1])
                    distanciaPen = calculaDistanciaPenalizada(distancia3d, matrizVertices[line - 1][column + 1], desvios, vetApp, vetInundacao, vetInclinacao)
                    self.insereAresta(indexOrigem, matrizVertices[line - 1][column + 1].id - 1, distancia3d, distanciaPen)
                #8 vizinho
                if (line + 1) < MAX_LINE_SIZE and (column + 1) < MAX_COLUMN_SIZE_NEXT:
                    distancia3d = calculaDistancia(origem, matrizVertices[line + 1][column + 1])
                    distanciaPen = calculaDistanciaPenalizada(distancia3d, matrizVertices[line + 1][column + 1], desvios, vetApp, vetInundacao, vetInclinacao)
                    self.insereAresta(indexOrigem, matrizVertices[line + 1][column + 1].id - 1, distancia3d, distanciaPen)

                column = column + 1

            MAX_COLUMN_SIZE_ANT = MAX_COLUMN_SIZE

        # for i in range(NUM_VERTICES):
        #     for j in range(NUM_VERTICES):
        #         distancia = calculaDistancia(area, i , j, 0)

        #         if distancia > 0 and distancia <= 80: #o parametro da distancia muda conforme os pixels da camada
        #             distancia3d = calculaDistancia(area, i, j, 1)
        #             #TODO: penalizacao de desvios, APP, inundacao e inclinacao

        #             #insere a aresta
        #             self.insereAresta(i, j, distancia3d, 1)

    def procuraMenorDistancia(self, peso, visitado):
        menor = -1
        primeiro = 1
        for i in range(self.nro_vertices):
            #procura vertice com menor distancia que nao tenha sido visitado
            if peso[i] >= 0 and visitado[i] == 0:
                if primeiro:
                    menor = i
                    primeiro = 0
                else:
                    if peso[menor] > peso[i]:
                        menor = i
        return menor


    def Dijkstra(self, orig, dest) -> SolucaoRoad:
        tinicio = time.time()
        sol = SolucaoRoad(self.nro_vertices)
        sol.cicloNegativo = 0
        sol.estrada.inicio = orig
        sol.estrada.termino = dest
        #ant armazena o vertice anterior do vertice atual
        #dist armazena a distancia do vertice atual par ao vertice inicial
        cont = self.nro_vertices
        #cria vetor auxiliar e inicializa distancias e anteriores
        visitado = [0 for _ in range(self.nro_vertices)]
        for i in range(self.nro_vertices): 
            sol.antecessor[i] = -1
            sol.sucessor[i] = -1
            sol.distancia[i] = -1
            sol.peso[i] = -1
        
        sol.distancia[sol.estrada.inicio] = 0
        sol.peso[sol.estrada.inicio] = 0
        while cont > 0:
            #procure vertices com menor distancia e marca como visitado
            u = self.procuraMenorDistancia(sol.peso, visitado)
            if u == -1:
                break
            visitado[u] = 1
            cont = cont - 1
            for i in range(self.grau[u]):
                #para cada vertice vizinho
                ind = self.arestas[u][i]
                #atualizar distancias dos vizinhos
                if sol.peso[ind] < 0:
                    sol.distancia[ind] = sol.distancia[u] + self.distancia[u][i]
                    #ou peso da aresta
                    sol.peso[ind] = sol.peso[u] + self.pesos[u][i]
                    sol.antecessor[ind] = u
                else:
                    if sol.peso[ind] > (sol.peso[u] + self.pesos[u][i]):
                        sol.distancia[ind] = sol.distancia[u] + self.distancia[u][i]
                        # ou peso da aresta
                        sol.peso[ind] = sol.peso[u] + self.pesos[u][i]
                        sol.antecessor[ind] = u
        #contando os vertices da rota
        sol.numVerticesRota = 0
        fim = sol.estrada.termino
        while fim != -1:
            sol.sucessor[sol.antecessor[fim]] = fim
            sol.verticesRoad.insert(0,fim)
            fim = sol.antecessor[fim]
            sol.numVerticesRota = sol.numVerticesRota + 1
        sol.FO = sol.peso[sol.estrada.termino]
        sol.distanciaTotal = sol.distancia[sol.estrada.termino]
        sol.tempo = (time.time() - tinicio) / 100.00
        sol.tempoSol = sol.tempo
 
        return sol
    