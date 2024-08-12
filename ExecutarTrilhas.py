import random
from math import inf
from typing import List, Optional
from .Services.commons import buscaAPP, calculaDistancia, calculaDistancia2D
from .Models.SolucaoTrails import SolucaoTrails, SolucaoPtTrails
from .Models.Grafo import Grafo
from .Models.SolucaoRoad import SolucaoRoads, SolucaoRoad
from .Models.ArvoreExploravel import ArvoreExploravel
from .Models.Patio import Patio
from .Models.SolucaoStorageYard import SolucaoStorageYard
from .Models.Area import Area
from .Models.Desvio import Desvio
from .Services.Draw import geraTrilhas
import copy

INFINITY = inf
EULER = 2.718281828459045235360287
PENALIZACAO_VOLUME = 1000
DISTANCIA_MAXIMA = 379
NUM_ITERACOES = 20000
TAXARESFRIAMENTO_TRAIL = 0.99
ITERACOES_VIZINHANCA_TRAIL = 50
TEMPERATURA_INICIAL_TRAIL = 10
TEMPERATURA_CONGELAMENTO_TRAIL = 0.1
GRAU_MAX = 8
PONDERADO = 1

def localizarVerticesVizinhos(area: List[Area], patios: List[Patio], verticesProibidos: List[int], patioAtual: int, distancia: float, vertPatios: List[int], NUM_VERTICES: int) -> int:
    distancia3d = 0.0
    j = 0
    for i in range(NUM_VERTICES):
        distancia3d = calculaDistancia2D(area[patios[patioAtual - 1].vertice - 1], area[i]) 
        if(distancia3d > 0 and distancia3d <= distancia and verticesProibidos[i] == 0):
            vertPatios[j] = i + 1
            j = j + 1
    return j
    
def calcularFOTrilha(vertPatios: List[int], qtdTrilhas: int, qtdArvPatio: int, area: List[Area], floresta: List[ArvoreExploravel], distancias: List[List[float]], solPtTtrails: SolucaoPtTrails, restVolSup: float) -> SolucaoPtTrails:
    diferencaVolume = 0
    diferencaDistancia = 0
    distanciaTotal = 0 #Variavel responsavel por armazenar a melhor distancia total
    
    res = copy.deepcopy(solPtTtrails)

    for i in range(qtdTrilhas):
        res.volumes[i] = 0.0
    
    # comparando as distancias dos pontos aleatorios
    for j in range(qtdArvPatio):
        distanciaMenor = INFINITY
        patio = 0
        for k in range(qtdTrilhas):
            distancia =  calculaDistancia(area[vertPatios[res.patios[k] - 1] - 1], floresta[j] )
            if distancia < distanciaMenor:
                distanciaMenor = distancia
                patio = k
        
        if distanciaMenor > DISTANCIA_MAXIMA:
            diferencaDistancia = diferencaDistancia + distanciaMenor - DISTANCIA_MAXIMA
        distanciaTotal = distanciaTotal + distanciaMenor

        #preencher volume por patio
        res.volumes[patio] = res.volumes[patio] + floresta[j].volume
    
    for w in range(qtdTrilhas):
        diferencaVolume += (res.volumes[w] - restVolSup) if (res.volumes[w] >= restVolSup) else 0
    
    res.distanciaTotal = distanciaTotal
    #penalizando solucao inviavel
    distanciaTotal += PENALIZACAO_VOLUME * (diferencaVolume + diferencaDistancia)

    res.FO = distanciaTotal
    res.viavel = ((diferencaVolume + diferencaDistancia) == 0)
    return res

def obterSolAleTrilha(vertPatios: List[int], qtdPatios: int, qtdTrilhas: int, qtdArvPatio: int, area: List[Area], floresta: List[ArvoreExploravel], distancias: List[List[float]], restVolSup: float) -> SolucaoPtTrails:
    patios = [0 for _ in range(qtdPatios)] #Vetor que vai guardar a informacao dos patios que ja foram selecionados
    solPtTtrails = SolucaoPtTrails()

    #gera os numeros aleatorios de acordo com o numero de trilhas
    for i in range(qtdTrilhas):
        #garante que sera gerado um numero aleatorio sem repeticoes
        while True:
            patio = 1 + ( random.randint( 0, qtdPatios - 1))
            
            if patios[patio - 1] != 1:
                break
        
        #depois de secionar um numero, marca ele como ja tendo sido selecionado e atribui ao patio
        patios[patio - 1] = 1
        solPtTtrails.patios[i] = patio
  
    solPtTtrails = calcularFOTrilha(vertPatios, qtdTrilhas, qtdArvPatio, area, floresta, distancias, solPtTtrails, restVolSup)
    return solPtTtrails

def heuConstIterTrilha(vertPatios: List[int], qtdPatios: int, qtdTrilhas: int, qtdArvPatio: int, area: List[Area], floresta: List[ArvoreExploravel], distancias: List[List[float]], num_iteracoes: int,restVolSup: float) -> SolucaoPtTrails:
    #tInicio = get_time()
    count = 0
    contViaveis = 0
    res = SolucaoPtTrails()
    melhorSol = SolucaoPtTrails()
    melhorSol.FO = INFINITY
    melhorSol.numViaveis = 0
    melhorSol.numInviaveis = 0

    #laco que faz a busca aleatoria e gulosa
    for _ in range(num_iteracoes):
        count = count + 1
        res = obterSolAleTrilha(vertPatios, qtdPatios, qtdTrilhas, qtdArvPatio, area, floresta, distancias, restVolSup)
        if res.FO < melhorSol.FO:
            melhorSol = res
            #melhorSol.tempoSol = (get_time() - tInicio / 100.00)
        
        if res.viavel:
            contViaveis = contViaveis + 1
    
    #melhorSol.tempo = (get_time() - tInicio) / 100.00
    melhorSol.numIteracoes = count
    melhorSol.numViaveis = contViaveis
    melhorSol.numInviaveis = count - contViaveis

    return melhorSol

def gerarVizinhoTrilha(vertPatios, qtdPatios, qtdTrilhas, qtdArvPatio, area, floresta, distancias, solPtrilhas, patios, restVolSup):
    solAtual = copy.deepcopy(solPtrilhas)
    #obtendo a posicao aletoria da troca
    troca = random.randint(0, qtdTrilhas - 1)
    
    while True:
        vizinho = 1 + (random.randint(0, qtdPatios-1))
        solAtual.patios[troca] = vizinho

        if patios[vizinho - 1] != 1:
            break
    
    #depois de selecionar um numero, marca ele como ja tendo sido selecionado
    patios[vizinho - 1] = 1

    solAtual = calcularFOTrilha(vertPatios, qtdTrilhas, qtdArvPatio, area, floresta, distancias, solAtual, restVolSup)
    return solAtual

def SATrails(vertPatios: List[int], qtdPatios: int, qtdTrilhas:int, qtdArvPatio:int, area: List[Area], floresta: List[ArvoreExploravel], distancias: List[List[float]], solInicial: SolucaoPtTrails, restVolSup:float):
    # tInicio = get_time()
    cont = 0
    countViaveis = 0
    countInviaveis = 0

    vizinho = SolucaoPtTrails()
    melhorSol = copy.deepcopy(solInicial)
    solucaoInicial = copy.deepcopy(solInicial)

    #vetor que vai guardar a informacao dos patios que ja foram selecionados
    patios = [0 for _ in range(qtdPatios)]

    #marcanco com 1 os elementos da solucao inicial
    for k in range(qtdTrilhas):
        patio = solucaoInicial.patios[k]
        patios[patio - 1] = 1
    
    #inicializando variaveis
    IterTemp = 0                        #numero de iteracoes na temperatura t
    temp = TEMPERATURA_INICIAL_TRAIL    #temperatura corrente

    while temp > TEMPERATURA_CONGELAMENTO_TRAIL:
        while IterTemp < ITERACOES_VIZINHANCA_TRAIL:
            IterTemp = IterTemp + 1
            cont = cont + 1
            vizinho = gerarVizinhoTrilha(vertPatios, qtdPatios, qtdTrilhas, qtdArvPatio, area, floresta, distancias, solucaoInicial, patios, restVolSup)
            #obtendo a variacao da solucao inicial para o vizinho
            variacao = vizinho.FO - solucaoInicial.FO

            if vizinho.viavel:
                countViaveis = countViaveis + 1
            else:
                countInviaveis = countInviaveis + 1
            
            #atualizando matriz de patios
            for i in range(qtdPatios):
                patios[i] = 0
            #se a variacao menor que zero, entao melhorou
            if variacao < 0:
                #melhorou a solucao inicial em relacao ao vizinho
                solucaoInicial = vizinho
                for i in range(qtdTrilhas):
                    patio = vizinho.patios[i]
                    patios[patio - 1] = 1
                
                if vizinho.FO < melhorSol.FO:
                    #melhorou a melhor solucao ate o momento em relacao ao vizinho
                    melhorSol = vizinho
                    #melhorSol.tempoSol = (get_time() - tInicial) / 100.0
            else:
                x = (random.randint(0, 1000))
                x = x / 1000
                if x < pow(EULER, (-variacao / temp)):
                    #atualiza matriz da solucao atual
                    #pega o vizinho mesmo este nao sendo melhor
                    solucaoInicial = vizinho
                    for i in range(qtdTrilhas):
                        patio = vizinho.patios[i]
                        patios[patio - 1] = 1
                else:
                    #corrige solucao atual
                    for j in range(qtdTrilhas):
                        patio = solucaoInicial.patios[j]
                        patios[patio - 1] = 1
        temp = TAXARESFRIAMENTO_TRAIL * temp
        IterTemp = 0
    #melhorSol.tempo = (get_time() - tInicio) / 100.0
    melhorSol.numIteracoes = cont
    melhorSol.numViaveis = countViaveis
    melhorSol.numInviaveis = countInviaveis

    return melhorSol

def atualizaVerticesTrilhas(grPatio: Grafo, solPtTrilhas, solTrilha, vInicioTrilha, qtdTrilhas, vInicial, vTrilhaOrder, vDistTrilha):
    vAtual = solTrilha.estrada.termino
    
    while vAtual != solTrilha.estrada.inicio:
        for i in range(qtdTrilhas):
            pontoTrilha = solPtTrilhas.patios[i]
            temp = grPatio.Dijkstra(vAtual, pontoTrilha)
            distanciaPontoTrilha = temp.FO

            temp = grPatio.Dijkstra(vAtual, vInicioTrilha)
            distanciaTrilhaPatio = temp.FO

            temp = grPatio.Dijkstra(vInicioTrilha, pontoTrilha)
            distanciaPontoPatio = temp.FO

            if distanciaTrilhaPatio < distanciaPontoPatio:
                if distanciaPontoTrilha < vDistTrilha[i]:
                    vTrilhaOrder[i] = vAtual
                    vDistTrilha[i] = distanciaPontoTrilha
        
        vAtual = solTrilha.antecessor[vAtual]
        if vAtual == -1:
            break

def trailsAprovTrilhas(grPatio: Grafo, area: List[Area], desvios: Optional[List[Desvio]], patioAtual: int, qtdTrilhas: int, solPtTrilhas: SolucaoPtTrails, arestasPatios: List[int], NUM_VERTICES: int):
    solTrilha = SolucaoRoad(NUM_VERTICES)
    #tInicio = get_time()
    sol = cria_SolTrails(qtdTrilhas, NUM_VERTICES)
    sol.patio = patioAtual
    sol.distanciaTotal = 0
    sol.FOTotal = 0
    sol.tempoTotal = 0

    #Tracado de trilhas de arraste
    pInicioTrilha = 0

    vTrilhaOrder = [-1 for _ in range(qtdTrilhas)]
    vDistTrilha = [INFINITY for _ in range(qtdTrilhas)]
    
    for i in range(qtdTrilhas):
        #tInicioTrilha = get_time()
        pTerminoTrilha = solPtTrilhas.patios[i]
        #obtendo as distancias
        temp = grPatio.Dijkstra(pInicioTrilha, pTerminoTrilha)
        vDistanciaPonto = temp.FO
        #trilha
        vTrilha = vTrilhaOrder[i]
        vDistanciaTrilha = vDistTrilha[i]

        if vDistanciaTrilha != 0:
            if vDistanciaPonto <= vDistanciaTrilha:
                solTrilha = grPatio.Dijkstra(pInicioTrilha, pTerminoTrilha)
            else:
                solTrilha = grPatio.Dijkstra(vTrilha, pTerminoTrilha)
            atualizaVerticesTrilhas(grPatio, solPtTrilhas, solTrilha, pInicioTrilha, qtdTrilhas, i+1, vTrilhaOrder, vDistTrilha)
        else:
            #gera uma solucao vazia
            solTrilha.estrada.inicio = vTrilha
            solTrilha.estrada.termino = pTerminoTrilha
            solTrilha.antecessor[vTrilha] = -1
            solTrilha.sucessor[vTrilha] = -1
            solTrilha.distancia[vTrilha] = 0
            solTrilha.peso[vTrilha] = 0
            solTrilha.numVerticesRota = 0
            solTrilha.FO = 0
            solTrilha.distanciaTotal = 0
        
        #solTrilha.tempo = solTrilha.tempoSol = (get_time() - tInicioTrilha) / 100.0
        sol.FOTotal = sol.FOTotal + solTrilha.FO
        sol.distanciaTotal = sol.distanciaTotal + solTrilha.distanciaTotal
        sol.roads[i] = solTrilha
    
    #sol.tempoTotal = (get_time() - tInicio) / 100.0
    return sol

def cria_SolTrails(nro_trails, NUM_VERTICES) -> SolucaoTrails:
    sol = SolucaoTrails()

    sol.roads = [SolucaoRoad(NUM_VERTICES) for _ in range(nro_trails)]

    return sol

class ExecutarTrilhas:
    
    def trails(self, area: List[Area], solRoads: SolucaoRoads, patios: List[Patio], solPatios: SolucaoStorageYard, floresta: List[ArvoreExploravel], arvoreSelPatios: List[List[int]], distancias: List[List[float]], app: Optional[List[int]], qtdArvores: List[int], restVolSup: float, desvios: Optional[List[Desvio]], NUM_VERTICES, NUM_PATIOS, NUM_ROADS, NUM_ARVORES_EXPLORAVEIS, NUM_ARV_TRILHA): 
        #tInicial = get_time()
        tempoYardTotal = 0.0
        distanciaYardMedia = 0.0
        FOYardTotal = 0.0
        tempoRoadTotal = 0.0
        distanciaRoadTotal = 0.0
        FORoadTotal = 0.0

        solucaoTrilha: List[SolucaoTrails] =[]
        roadPatio = SolucaoRoad(NUM_VERTICES)
        grPatio = Grafo()
        
        #pre-processamento - marcando os vertices de estrada proibidos
        #zerando
        verticesProibidos = [0 for _ in range(NUM_VERTICES)]

        if(app != None):
            print("App existe")
            #marcando os vertices de APPs como proibidos
            for i in range(NUM_VERTICES):
                if buscaAPP(app, i):
                    verticesProibidos[i] = 1
        
        #marcando os vertices ja utilizados em estradas como proibidos
        for i in range(NUM_ROADS):
            vAtual = solRoads.roads[i].estrada.termino
            while (vAtual != -1):
                verticesProibidos[vAtual] = 1
                vAtual = solRoads.roads[i].antecessor[vAtual]
   
        #percorrendo os patios para definir as trilhas em cada patio
        for i in range(NUM_PATIOS):
            solPtTrilhas = SolucaoPtTrails()
            arvMaisDistante = 0.0
            patioAtual = solPatios.patios[i]

            qtdTrilhas = int((qtdArvores[i] / NUM_ARV_TRILHA)) if ((qtdArvores[i] / NUM_ARV_TRILHA) >= 1 ) else 1
            #definindo o vetor subPatios
            vSubArvPatios = [ArvoreExploravel() for _ in range(qtdArvores[i])]
            vSubDistPatios = [0.0 for _ in range(qtdArvores[i])]
            k = 0


            for j in range (NUM_ARVORES_EXPLORAVEIS):
                if arvoreSelPatios[i][j] == 1:
                    vSubArvPatios[k] = floresta[j]
                    vSubDistPatios[k] = distancias[j][patioAtual - 1]
                    if distancias[j][patioAtual - 1] > arvMaisDistante:
                        arvMaisDistante = distancias[j][patioAtual - 1]
                    k = k + 1
            
            #construindo a area do patio
            areaPatio = (arvMaisDistante / int(30)) + 1

            qtdVerticesPatio = pow((areaPatio * 2), 2)
            vertPatios = [0 for _ in range( int(qtdVerticesPatio))]
            #localizando os vertices vizinhos
            qtdRealVertPatio = localizarVerticesVizinhos(area, patios, verticesProibidos, patioAtual, arvMaisDistante, vertPatios, NUM_VERTICES)
            
            #TODO:
            # Ver se isso esta correto, pois qtdRealVertPatio esta sendo 0 em alguns momentos, e por causa da solucao falha de patios?
            
            if(qtdRealVertPatio == 0):
                print("\n\n\npatioAtual: " + str(patioAtual) + " \nqtdRealVertPatio = 0\n\n\n")
            else:

                vertRealPatios = [0 for _ in range(qtdRealVertPatio)]
                for j in range(qtdRealVertPatio):
                    vertRealPatios[j] = vertPatios[j] #vertRealPatios recebe id de cada vertice proximo do patio

                #obtendo os pontos para as trilhas
                solPtTrilhas = heuConstIterTrilha(vertRealPatios, qtdRealVertPatio, qtdTrilhas, qtdArvores[i], area, vSubArvPatios, distancias, NUM_ITERACOES, restVolSup)
                solPtTrilhas.__str__()

                solPtTrilhas = SATrails(vertRealPatios, qtdRealVertPatio, qtdTrilhas, qtdArvores[i], area, vSubArvPatios, distancias, solPtTrilhas, restVolSup)
                
                tempoYardTotal = tempoYardTotal + solPtTrilhas.tempoSol
                FOYardTotal = FOYardTotal + solPtTrilhas.FO

                #construindo grafo 
                qtdRealVertPatio = qtdRealVertPatio + 1
                vertArestaPatios = [0 for _ in range(qtdRealVertPatio)]
                vertArestaPatios[0] = patios[patioAtual - 1].vertice
                for j in range(1, qtdRealVertPatio):
                    vertArestaPatios[j] = vertRealPatios[j - 1]
                
                #criando o grafo do patio para neste grafo definir as trilhas
                grPatio.cria_Grafo(qtdRealVertPatio, GRAU_MAX, PONDERADO)
                grPatio.insereArestasPatios(area, vertArestaPatios, qtdRealVertPatio, desvios)
                #definindo as trilhas no grafo do patio
                sol = trailsAprovTrilhas(grPatio, area, desvios, patioAtual, qtdTrilhas, solPtTrilhas, vertArestaPatios, NUM_VERTICES)

                distanciaRoadTotal = sol.distanciaTotal + distanciaRoadTotal
                FORoadTotal = sol.FOTotal + FORoadTotal

                for road in sol.roads:
                    aux = []
                    for vertice in road.verticesRoad:
                        aux.append(vertArestaPatios[vertice]-1)
                    road.verticesRoad = copy.copy(aux)
                
                solucaoTrilha.append(sol)
            
        #tempoRoadTotal = (get_time() - tfInicio) / 100.0
        distanciaYardMedia = distanciaYardMedia + (FOYardTotal / NUM_ARVORES_EXPLORAVEIS)
        print("-------- Resultado final de locais -------- ")
        print( "Distancia media\t Fo total\t Tempo (s)\n")
        print( str(distanciaYardMedia)+" \t")
        print( str(FOYardTotal)+"\t")
        print( str(tempoYardTotal)+"\n")

        print("-------- Resultado final de trilhas --------")
        print( "Distancia media\t Fo total\t Tempo (s)\n")
        print( str(distanciaRoadTotal)+" \t")
        print( str(FORoadTotal)+"\t")
        print( str(tempoRoadTotal)+"\n")

        return solucaoTrilha
