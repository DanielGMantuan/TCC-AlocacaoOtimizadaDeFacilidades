import math
from ..Models.Patio import Patio
from ..Models.Area import Area
from ..Models.Desvio import Desvio
from ..Models.Inclinacao import Inclinacao
from ..Models.ArvoreRemanescente import ArvoreRemanescete
from ..Models.ArvoreExploravel import ArvoreExploravel
from .commons import buscapatio, buscaPatioInLayer
from typing import List

class PreProcLayer:
    def __init__(self, NUM_VERTICES):
        self.numVertices = NUM_VERTICES

    def lerInstanciaVertices(self, vertices) -> list[Area]:
        vetor: list[Area] = []

        for verticeLayer in vertices.getFeatures():
            vertice = Area()

            vertice.id = int(verticeLayer.attribute("id"))
            vertice.x = float(verticeLayer.attribute("x"))
            vertice.y = float(verticeLayer.attribute("y"))
            vertice.z = float(verticeLayer.attribute("z"))
            
            vetor.append(vertice)
        
        return vetor
    
    def lerInstanciaArvoresRemanescentes(self, floresta) -> list[Desvio]:
        desvios: list[Desvio] = []

        for arvore in floresta.getFeatures():
            desvio = Desvio()
            
            # desvio.id = int(arvore.attribute("Id"))
            desvio.x = float(arvore.attribute("X_Este"))
            desvio.y = float(arvore.attribute("Y_Norte"))
            desvio.z = float(arvore.attribute("z"))

            desvios.append(desvio)
        
        return desvios

    def lerInstanciaInundacao(self, inundacao) -> list[int]:
        vetor: list[int] = [0 for _ in range(self.numVertices)]

        for verticeInund in inundacao.getFeatures():
            id = verticeInund.attribute("Id")
            vetor[id - 1] = 1
        
        return vetor
    
    def lerInstanciaAPP(self, app) -> list[int]:
        vetor: list[int] = [0 for _ in range(self.numVertices)]

        for verticeApp in app.getFeatures():
            id = verticeApp.attribute("Id")
            vetor[id - 1] = 1
        
        return vetor
    
    def lerInstanciaInclinacao(self, inclinacao) -> list[Inclinacao]:
        vetor: list[Inclinacao] = []

        for verticeInc in inclinacao.getFeatures():
            verticeInclinacao = Inclinacao()

            # verticeInclinacao.id = int(verticeInc.attribute("id"))
            verticeInclinacao.x = float(verticeInc.attribute("x"))
            verticeInclinacao.y = float(verticeInc.attribute("y"))
            verticeInclinacao.z = float(verticeInc.attribute("z"))
            verticeInclinacao.slope = verticeInc.attribute("inclinacao")

            vetor.append(verticeInclinacao)
        
        return vetor
    
    def lerInstanciaDistancias(self, arvDistancias, NUM_ARVORES, NUM_PATIOS) -> list[list[float]]:
        matriz = [[0.0 for _ in range(NUM_PATIOS)] for _ in range(NUM_ARVORES)]

        for verticeInc in arvDistancias.getFeatures():
            idArvore = int(verticeInc.attribute("arvore"))
            idPatio = int(verticeInc.attribute("patio"))
            distancia = float(verticeInc.attribute("distancia_total"))

            matriz[idArvore-1][idPatio-1] = distancia
        
        return matriz

    def lerArquivoDistancias(self, filePath: str) -> list[list[float]]:
        matriz:list[list[float]] = []
        with open(filePath, 'r') as arquivo:
            for linha in arquivo:
                valores = linha.strip().split('\t')  # Divide os valores separados por tabulação
                linha = [float(valor.replace(',', '.').strip()) for valor in valores]  # Remove espaços e converte para float
                matriz.append(linha)
        return matriz

    def lerInstanciaPatiosDadosMarcelo(self, patios, area: list[Area]) -> list[Patio]:
        vetor: list[Patio] = []
        for patioLayer in patios.getFeatures():
            patio = Patio()
            patio.id = int(patioLayer.attribute("PT")) 
            patio.x = float( "{:.4f}".format(patioLayer.attribute("POINT_X")) )
            patio.y = float( "{:.3f}".format(patioLayer.attribute("POINT_Y")))
            # patio.z = float( "{:.4f}".format(patioLayer.attribute("z")))
            vertice = buscaPatioInLayer(patio, area)
            if(vertice != -1):
                patio.vertice = vertice
            else:
                raise Exception("Um patio nao tem equivalente no layer da area")
            vetor.append(patio)
        return vetor
    
    def lerInstanciaPatios(self, patios, area: list[Area]) -> list[Patio]:
        vetor: list[Patio] = []
        for patioLayer in patios.getFeatures():
            patio = Patio()
            patio.id = int(patioLayer.attribute("id")) 
            patio.x = float(patioLayer.attribute("x"))
            patio.y = float(patioLayer.attribute("y"))
            patio.z = float(patioLayer.attribute("z"))
            vertice = buscaPatioInLayer(patio, area)
            if(vertice != -1):
                patio.vertice = vertice
            else:
                raise Exception("Um patio nao tem equivalente no layer da area")
            vetor.append(patio)
        return vetor

    def lerInstanciaArvoresExploraveis(self, arvores) -> list[ArvoreExploravel]:
        vetor: list[ArvoreExploravel] = []

        for arvoreLayer in arvores.getFeatures():
            arvore = ArvoreExploravel()

            arvore.id = arvoreLayer.attribute("id")
            arvore.numero = arvoreLayer.attribute("N__Arvore")
            # arvore.DAP = arvoreLayer.attribute("DAP")
            # arvore.H = arvoreLayer.attribute("HC")
            # arvore.areaBasal = arvoreLayer.attribute("G")
            arvore.volume = arvoreLayer.attribute("Volume_Eq")
            arvore.x = arvoreLayer.attribute("X_Este")
            arvore.y = arvoreLayer.attribute("Y_Norte")
            arvore.z = arvoreLayer.attribute("Z")

            vetor.append(arvore)

        return vetor

    def matrizDistPatiosArv(self, patios: list[Patio], floresta_exp: List[ArvoreExploravel]):
        matriz = []

        for arvore in floresta_exp:
            linha = []
            for patio in patios:
                distancia = math.sqrt(math.pow((arvore.x - patio.x), 2) + math.pow((arvore.y - patio.y), 2))
                linha.append(distancia)
            matriz.append(linha)

        return matriz
    
    def criaVetorVolume(self, floresta_exp):
        vetor = []

        for arvore in floresta_exp.getFeatures():
            vetor.append(arvore.attribute("Volume"))

        return vetor

    def calculaVolume(self, arvoresExploraveis: list[ArvoreExploravel], NUM_ARVORES_EXPLORAVEIS):
        volumeTotal = 0

        for i in range(NUM_ARVORES_EXPLORAVEIS):
            volumeTotal = volumeTotal + arvoresExploraveis[i].volume

        return volumeTotal
    
    def referenciaVetVertices(self, vetPatio, listSolPatios, vetVeticesID):
        vetor = []
        for solPatio in listSolPatios:
            for vertice in vetVeticesID:
                if (vetPatio[solPatio][0] == vertice[1]) and (vetPatio[solPatio][1] == vertice[2]):
                    vetor.append(vertice[0] - 1)
                    break
        return vetor
    
    def vetPatiosReferenciaVetVertices(self, vetPatios, vetVetices):
        vetor =[]
        for patio in vetPatios:
            for vertice in vetVetices:
                if (patio[0] == vertice[0]) and (patio[1] == vertice[1]):
                    vetor.append(vertice)
                    break
        return vetor
