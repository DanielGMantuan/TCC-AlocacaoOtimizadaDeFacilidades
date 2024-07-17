from .Models.SolucaoRoad import SolucaoRoads, SolucaoRoad
from .Services.commons import calculaDistancia, buscapatio
from .Models.Grafo import Grafo
from .Services.PreProcecamentoRoads import PreProcecamentoRoads
from math import inf
from .Models.Area import Area
from .Models.SolucaoStorageYard import SolucaoStorageYard
from .Models.SolucaoRoad import AccessRoad
from .Models.Patio import Patio

NUM_VERTICES = 0
NUM_PATIOS = 0
NUM_ACCESS_ROAD = 0
NUM_ROADS = 0
INFINITY = inf

class RoadsAprovTrecho:
    def encontrarSubTrecho(self, roads: SolucaoRoads, definedRoads: list[int], estradaAtual: int):
        global NUM_ROADS
        for i in range(NUM_ROADS):
            #se a estrada nao foi definida ainda, entao entra
            if i != estradaAtual:
                if roads.roads[i].estrada.termino == roads.roads[estradaAtual].estrada.inicio: #a estrada termina no vertice de inico
                    #achou continuidade da estrada
                    roads.typeRoad[i] = 1
                    definedRoads[i] = 1
                    # self.encontrarSubTrecho(roads, definedRoads, i)
                    estradaAtual = i
                    i = 0

    def determinarTipoEstrada(self, roads: SolucaoRoads, defineRoads: list[int]):
        global NUM_ROADS
        #encontrar as estradas primarias
        for i in range(NUM_ROADS):
            if roads.typeRoad[i] == 1:
                self.encontrarSubTrecho(roads, defineRoads, i)

    def obterVerticeInicioProximo(self, area: list[Area], estradasAcesso: AccessRoad, vertice: int, vDistEstPri: list[float]):
        vMenor = -1
        dMenor = INFINITY
        
        for i in range(NUM_ACCESS_ROAD):
            inicio = estradasAcesso.inicio[i]
            distancia = calculaDistancia(area[vertice], area[inicio])
            if distancia < dMenor:
                vMenor = inicio
                dMenor = distancia
        vDistEstPri[0] = dMenor
        return vMenor

    def atualizaVerticesEstSecundarias(self, area: list[Area], patios: list[Patio], solPatios: SolucaoStorageYard, solRoadSec: SolucaoRoad, estradasAcesso: AccessRoad, vEstSecOrder: list[int], vDistEstSec: list[float], vInicial: int, vPatProibido: int):
        # O objetivo dessa funcao e incluir as novas estradas
        # secundarias que foram tratadas ate o momento nas rotas
        # possiveis para os patios que ainda precisam ser alocados

        distInicio = [0.0]
        vAtual = solRoadSec.antecessor[solRoadSec.estrada.termino]
        while vAtual != solRoadSec.estrada.inicio and vAtual != -1:
            for i in range(vInicial, NUM_PATIOS):
                if vPatProibido != solPatios.patios[i]:
                    vPatio = patios[solPatios.patios[i] - 1].vertice -1

                    #obtendo o vertice de inicio proximo do patio atual
                    inicio = self.obterVerticeInicioProximo(area, estradasAcesso, vPatio, distInicio)
                    #calcula a distancia do vertice atual para o patio atual
                    distancia = calculaDistancia(area[vAtual], area[vPatio])
                    #calcula a distancia do vertice atual para o inicio mais proximo
                    distVert = calculaDistancia(area[vAtual], area[inicio])

                    if distVert < distInicio[0]:
                        #se a distancia do vertice para o inicio e menor que a distancia do patio ate o inicio
                        #executa para assim garantir o fluxo
                        if vEstSecOrder[i] == -1:
                            #se o patio atual nao tem nenhum vertice proximo
                            vEstSecOrder[i] = vAtual
                            vDistEstSec[i] = distancia
                        else:
                            if distancia < vDistEstSec[i]:
                                #verifica se a distancia atual e menor que a nova calculada
                                vEstSecOrder[i] = vAtual
                                vDistEstSec[i] = distancia
            vAtual = solRoadSec.antecessor[vAtual]

    def obterPatioProximo(self, area: list[Area], patios: list[Patio], vertEst: int, distPatioEst: float, idxPatio: int, distanciasPatios: list[list[float]], patiosOrder: list[list[int]], distancia: list[float]):
        retorno = -1
        iPatio = 1
        patioCon = -1
        while ((patioCon == -1) and (iPatio < NUM_PATIOS)):
            patioCon = patiosOrder[idxPatio][iPatio]
            vDistPat = distanciasPatios[idxPatio][iPatio]
            if patioCon != -1:
                distEst = calculaDistancia(area[vertEst], patios[patioCon - 1])
                if distEst < distPatioEst:
                    distancia[0] = vDistPat
                    return patioCon
            iPatio = iPatio + 1
        return retorno

    def roadsAprovTrecho(self, grafo: Grafo, area: list[Area], patios: list[Patio], solPatios: SolucaoStorageYard, estradasAcesso: AccessRoad, num_patios: int, num_vertices: int, num_access_road: int): 
        global NUM_PATIOS, NUM_VERTICES, NUM_ROADS, NUM_ACCESS_ROAD
        NUM_PATIOS= num_patios 
        NUM_VERTICES = num_vertices
        NUM_ROADS = NUM_PATIOS + 1
        NUM_ACCESS_ROAD = num_access_road

        patioProibido = -1
        solRoad = SolucaoRoad(NUM_VERTICES)
        sol = SolucaoRoads(NUM_ROADS, NUM_VERTICES)
        vEstSecOrder = [-1 for _ in range(NUM_PATIOS)]
        vDistEstradaSec = [INFINITY for _ in range(NUM_PATIOS)]
        vetSelRoads = [0 for _ in range(NUM_ROADS)]
        vDistPat = [0.0]
        vDistEstPri = [0.0]

        #executando o preprocessamento das roads
        preRods = PreProcecamentoRoads(NUM_PATIOS, patios, solPatios)
        distanciaPatios = preRods.distanciaPatios
        patiosOrder = preRods.patiosOrder

        #ligando os patios com as estradas de acesso
        for i in range(NUM_ACCESS_ROAD):
            vEstradaPri = estradasAcesso.inicio[i]
            pMenor = -1
            patioCon = -1
            menor = INFINITY

            #verificando qual patio esta mais proximo
            for j in range(NUM_PATIOS):
                patioAtual = solPatios.patios[j]
                vPatioAtual = patios[patioAtual - 1].vertice - 1
                vDistPat[0] = calculaDistancia(area[vEstradaPri], area[vPatioAtual])
                if (vDistPat[0] < menor):
                    patioCon = j
                    pMenor = vPatioAtual
                    menor = vDistPat[0]
            
            #Realiza a ligacao ate a estrada primaria
            solRoad = grafo.Dijkstra(pMenor, vEstradaPri)
            typeRoad = 1
            vetSelRoads[patioCon] = 1

            #atualiza os vertices das estradas secundarias em relacao aos patios
            self.atualizaVerticesEstSecundarias(area, patios, solPatios, solRoad, estradasAcesso, vEstSecOrder, vDistEstradaSec, 0, patioProibido)
            sol.roads[patioCon] = solRoad
            sol.typeRoad[patioCon] = typeRoad
            sol.tempoTotal += solRoad.tempo
            sol.distanciaTotal += solRoad.distanciaTotal
            sol.FOTotal += solRoad.FO
        
        pMenor = -1
        menor = INFINITY
        
        #ligando os patios as estradas e outros patios
        for i in range(NUM_PATIOS):
            #apenas patios que nao foram ligados ainda
            if vetSelRoads[i] == 0:
                patioProibido = -1
                patioAtual = solPatios.patios[i]    #equivale ao id dos patios
                vPatioAtual = patios[patioAtual - 1].vertice - 1   
                #estrada primaria
                vEstradaPri = self.obterVerticeInicioProximo(area, estradasAcesso, vPatioAtual, vDistEstPri)
                #estrada secundaria
                vEstradaSec = vEstSecOrder[i]
                vDistEstSec = vDistEstradaSec[i]

                #verifica se o patio esta em algum vertice da estrada principal
                if vDistEstPri[0] != 0 and vDistEstSec != 0:
                    patioCon = self.obterPatioProximo(area, patios, vEstradaPri, vDistEstPri[0], i, distanciaPatios, patiosOrder, vDistPat)
                    
                    if patioCon != -1:
                        if vDistEstPri[0] <= vDistEstSec and vDistEstPri[0] <= vDistPat[0]:
                            #realiza a ligacao ate a estrada primaria
                            solRoad = grafo.Dijkstra(vPatioAtual, vEstradaPri)
                            typeRoad = 1
                            vetSelRoads[i] = 1 
                        elif vDistEstSec <= vDistEstPri[0] and vDistEstSec <= vDistPat[0]:
                            #realiza a ligacao ate a estrada secundaria
                            solRoad = grafo.Dijkstra(vPatioAtual, vEstradaSec)
                            typeRoad = 2
                            vetSelRoads[i] = 1
                        else:
                            #realiza a ligacao ate outro patio
                            solRoad = grafo.Dijkstra(vPatioAtual, patios[patioCon - 1].vertice - 1)
                            typeRoad = 2
                            #cria uma ligacao inversa proibida are os dois patios
                            patioProibido = patioCon
                            for j in range(i+1, NUM_PATIOS):
                                if patioCon == solPatios.patios[j]:
                                    #marcando o proximo patio na busca
                                    for k in range(1, NUM_PATIOS):
                                        if patiosOrder[j][k] == patioAtual:
                                            patiosOrder[j][k] = -1
                                            break
                                    break
                    else:
                        if vDistEstPri[0] <= vDistEstSec:
                            #realiza a ligacao ate a estrada primaria
                            solRoad = grafo.Dijkstra(vPatioAtual, vEstradaPri)
                            typeRoad = 1
                            vetSelRoads[i] = 1
                        else:
                            #realiza a ligacao ate a estrada secundaria

                            solRoad = grafo.Dijkstra(vPatioAtual, vEstradaSec)
                            typeRoad = 2
                            vetSelRoads[i] = 1
                    #atualiza os vertices das estradas secundaria em relacao aos patios
                    self.atualizaVerticesEstSecundarias(area, patios, solPatios, solRoad, estradasAcesso, vEstSecOrder, vDistEstradaSec, i+1, patioProibido)
                    sol.roads[i] = solRoad
                    sol.typeRoad[i] = typeRoad
                    sol.tempoTotal += solRoad.tempo
                    sol.distanciaTotal += solRoad.distanciaTotal
                    sol.FOTotal += solRoad.FO
                else:
                    #gera uma solucao vazia
                    solRoad.estrada.inicio = vPatioAtual
                    solRoad.estrada.termino = vPatioAtual
                    solRoad.antecessor[vPatioAtual] = -1
                    solRoad.sucessor[vPatioAtual] = -1
                    solRoad.distancia[vPatioAtual] = 0
                    solRoad.peso[vPatioAtual] = 0
                    solRoad.numVerticesRota = 0
                    solRoad.FO = 0
                    solRoad.distanciaTotal = 0
                    solRoad.tempo = 0
                    solRoad.tempoSol = 0
                    sol.typeRoad[i] = 1
                    sol.roads[i] = solRoad
                    vetSelRoads[i] = 1; 
        #ligando o vertice da saida da UT   
        if estradasAcesso.termino != 0:
            for i in range(NUM_PATIOS):
                patioAtual = solPatios.patios[i]
                vPatioAtual = patios[patioAtual - 1].vertice - 1
                vDistPat[0] = calculaDistancia(area[vPatioAtual], area[estradasAcesso.termino])
                if vDistPat[0] < menor:
                    pMenor = vPatioAtual
                    menor = vDistPat[0]
            #construindo o tracado final
            solRoad = grafo.Dijkstra(pMenor, estradasAcesso.termino)
            sol.typeRoad[i] = 1
            sol.roads[NUM_ROADS - 1] = solRoad
            sol.tempoTotal += solRoad.tempo
            sol.distanciaTotal += solRoad.distanciaTotal
            sol.FOTotal += solRoad.FO
            vetSelRoads[i] = 1
        else:
            #gera uma solu��o vazia
            solRoad.estrada.inicio = estradasAcesso.termino
            solRoad.estrada.termino = estradasAcesso.termino
            solRoad.antecessor[0] = -1
            solRoad.sucessor[0] = -1
            solRoad.distancia[0] = 0
            solRoad.peso[0] = 0
            solRoad.numVerticesRota = 0
            solRoad.FO = 0
            solRoad.distanciaTotal = 0
            solRoad.tempo = 0
            solRoad.tempoSol = 0
            sol.typeRoad[NUM_ROADS - 1] = 1
            sol.roads[NUM_ROADS - 1] = solRoad
            vetSelRoads[NUM_ROADS - 1] = 1
        self.determinarTipoEstrada(sol, vetSelRoads)
        return sol
