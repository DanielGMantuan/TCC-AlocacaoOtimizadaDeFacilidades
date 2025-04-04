from qgis.core import (
    QgsProject, 
    QgsVectorLayer, 
    QgsFeature,
    QgsField, 
    QgsGeometry, 
    QgsPointXY, 
    QgsLineString, 
    QgsMarkerSymbol, 
    QgsCoordinateReferenceSystem,
    QgsVectorFileWriter,
    QgsCoordinateTransformContext,
    QgsSingleSymbolRenderer
)
from qgis.PyQt.QtCore import QVariant
from PyQt5.QtGui import QColor

import shutil
import os
import random
from ..Models.SolucaoTrails import SolucaoTrails
from ..Models.ArvoreExploravel import ArvoreExploravel
from ..Models.SolucaoStorageYard import SolucaoStorageYard
    
def geraPontosMemoy(solPatios, patios, i):
    crs = QgsCoordinateReferenceSystem('EPSG:32766')
    camadaSolucao = QgsVectorLayer("point", "Solução " + str(i) , "memory")
    camadaSolucao.setCrs(crs)  # Defina o SRC da camada

    so = camadaSolucao.dataProvider()
    so.addAttributes([QgsField("ID", QVariant.Int),
                    QgsField("POINT_X", QVariant.Double),
                    QgsField("POINT_Y", QVariant.Double),
                    QgsField("ALTITUDE", QVariant.Double)])
    camadaSolucao.updateFields()

    # Define o tamanho do ponto e o símbolo
    ponto_simbolo = QgsMarkerSymbol.createSimple({'name': 'square', 'color': 'black', 'size': '2.5'})
    renderer = camadaSolucao.renderer()
    renderer.setSymbol(ponto_simbolo)
    camadaSolucao.triggerRepaint()

    for patio in patios.getFeatures():
        for idPatio in solPatios.patios:
            if idPatio == patio.attribute("id"):
                f = QgsFeature()
                f.setAttributes([patio.attribute("id"), patio.attribute("x"), patio.attribute("y"), patio.attribute("z")])
                f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(float(patio.attribute("x")), float(patio.attribute("y")))))
                so.addFeature(f)

    camadaSolucao.updateExtents()
    QgsProject.instance().addMapLayer(camadaSolucao)


def geraFilePontos(solPatios, patios, i):
    crs = QgsCoordinateReferenceSystem('EPSG:31981')

    # Criar a camada vetorial
    camadaSolucao = QgsVectorLayer("point", "Solução " + str(i), "memory")
    camadaSolucao.setCrs(crs)  # Defina o SRC da camada

    # Adiciona atributos
    provider = camadaSolucao.dataProvider()
    provider.addAttributes([QgsField("ID", QVariant.Int),
                            QgsField("POINT_X", QVariant.Double),
                            QgsField("POINT_Y", QVariant.Double),
                            QgsField("ALTITUDE", QVariant.Double)])
    camadaSolucao.updateFields()

    # Define o tamanho do ponto e o símbolo
    ponto_simbolo = QgsMarkerSymbol.createSimple({'name': 'square', 'color': 'black', 'size': '2.5'})

    # Criação do renderizador de símbolo
    renderer = QgsSingleSymbolRenderer(ponto_simbolo)

    # Define o renderizador para a camada
    camadaSolucao.setRenderer(renderer)

    # Adiciona as features à camada
    for patio in patios.getFeatures():
        for idPatio in solPatios.patios:
            if idPatio == patio.attribute("id"):
                f = QgsFeature()
                f.setAttributes([patio.attribute("id"), patio.attribute("x"), patio.attribute("y"), patio.attribute("z")])
                f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(float(patio.attribute("x")), float(patio.attribute("y")))))
                provider.addFeature(f)
    
    nome_arquivo = r"C:\Users\NOTE155\Desktop\Iniciacao Cientifica\Resultados\Solucao" + str(i) + r"\patios.shp"
    diretorio = r"C:\Users\NOTE155\Desktop\Iniciacao Cientifica\Resultados\Solucao" + str(i)

    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "ESRI Shapefile"

    # Salvar a camada vetorial em um arquivo
    QgsVectorFileWriter.writeAsVectorFormatV2(camadaSolucao, nome_arquivo, QgsCoordinateTransformContext(), options)

    # Adicionar a camada ao projeto
    QgsProject.instance().addMapLayer(camadaSolucao)

def geraPontosPatiosMarcelo(solPatios, patios, i, path):
    crs = QgsCoordinateReferenceSystem('EPSG:31981')

    # Criar a camada vetorial
    camadaSolucao = QgsVectorLayer("point", "Solução " + str(i), "memory")
    camadaSolucao.setCrs(crs)  # Defina o SRC da camada

    # Adiciona atributos
    provider = camadaSolucao.dataProvider()
    provider.addAttributes([QgsField("PT", QVariant.Int),
                            QgsField("POINT_X", QVariant.Double),
                            QgsField("POINT_Y", QVariant.Double)])
    camadaSolucao.updateFields()

    # Define o tamanho do ponto e o símbolo
    ponto_simbolo = QgsMarkerSymbol.createSimple({'name': 'square', 'color': 'black', 'size': '2.5'})

    # Criação do renderizador de símbolo
    renderer = QgsSingleSymbolRenderer(ponto_simbolo)

    # Define o renderizador para a camada
    camadaSolucao.setRenderer(renderer)

    # Adiciona as features à camada
    for patio in patios.getFeatures():
        for idPatio in solPatios.patios:
            if idPatio == patio.attribute("id"):
                f = QgsFeature()
                f.setAttributes([patio.attribute("id"), patio.attribute("x"), patio.attribute("y")])
                f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(float(patio.attribute("x")), float(patio.attribute("y")))))
                provider.addFeature(f)
    
    nome_arquivo = fr"{path}\patio\patio.shp"
    diretorio = fr"{path}\patio"

    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "ESRI Shapefile"

    # Salvar a camada vetorial em um arquivo
    QgsVectorFileWriter.writeAsVectorFormatV2(camadaSolucao, nome_arquivo, QgsCoordinateTransformContext(), options)

    # # Adicionar a camada ao projeto
    QgsProject.instance().addMapLayer(camadaSolucao)
    # del camadaSolucao


def geraPontosArvores(solArvores: list[dict], arvores: list[ArvoreExploravel], numero, indexSolucao, path: str):
    crs = QgsCoordinateReferenceSystem('EPSG:31981')
    camadaSolucao = QgsVectorLayer("point", "arvores " + str(numero) , "memory")
    camadaSolucao.setCrs(crs)

    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    color = QColor(red, green, blue)

    so = camadaSolucao.dataProvider()
    so.addAttributes([QgsField("COD", QVariant.Int),
                    QgsField("POINT_X", QVariant.Double),
                    QgsField("POINT_Y", QVariant.Double)])
    camadaSolucao.updateFields()

    # Define o tamanho do ponto e o símbolo
    ponto_simbolo = QgsMarkerSymbol.createSimple({'name': 'circle', 'color': color, 'size': '2'})
    renderer = QgsSingleSymbolRenderer(ponto_simbolo)
    camadaSolucao.setRenderer(renderer)
    camadaSolucao.triggerRepaint()
    
    for i in range(len(solArvores)):
        f = QgsFeature()
        f.setAttributes([arvores[solArvores[i]['id'] - 1].id, arvores[solArvores[i]['id'] - 1].x, arvores[solArvores[i]['id'] - 1].y, arvores[solArvores[i]['id'] - 1].z])
        f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(float(arvores[solArvores[i]['id'] - 1].x), float(arvores[solArvores[i]['id'] - 1].y))))
        so.addFeature(f)


    nome_arquivo = fr"{path}\arvores\Arvores{str(numero)}.shp"
    diretorio = fr"{path}\arvores"

    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "ESRI Shapefile"

    # Salvar a camada vetorial em um arquivo
    QgsVectorFileWriter.writeAsVectorFormatV2(camadaSolucao, nome_arquivo, QgsCoordinateTransformContext(), options)

    # Adicionar a camada ao projeto
    del camadaSolucao
  
def geraVetorDePontos(verticesRoad, matVertices):
    road = []
    for vertice in verticesRoad:
        road.append(QgsPointXY(matVertices[vertice].x,matVertices[vertice].y))
    return road
    
def drawLine(colectionPointList, flag, i, path):
    crs = QgsCoordinateReferenceSystem('EPSG:31981')
    if(flag):
        vl = QgsVectorLayer("linestring", "Estradas", "memory")
    else:
        vl = QgsVectorLayer("linestring", "Trilhas", "memory")
        
    vl.setCrs(crs)

    vpr = vl.dataProvider()
    vpr.addAttributes([QgsField("Type", QVariant.String)])

    vl.updateFields()
    f = QgsFeature()
    f.setAttributes(["Principal"])
    for pointCollection in colectionPointList:
        f.setGeometry(QgsLineString(pointCollection))
        vpr.addFeature(f)
    vl.updateExtents() 
    QgsProject.instance().addMapLayer(vl)

    if(flag):
        nome_arquivo = fr"{path}\estradas\estrada.shp"
        diretorio = fr"{path}\estradas"

        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
        
    else:
        nome_arquivo = fr"{path}\trilhas\shapes\trilha.shp"
        diretorio = fr"{path}\trilhas"

        if not os.path.exists(diretorio):
            os.makedirs(fr"{path}\trilhas\shapes")
        

    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "ESRI Shapefile"
    QgsVectorFileWriter.writeAsVectorFormatV2(vl, nome_arquivo, QgsCoordinateTransformContext(), options)
    
def drawLine1(colectionPointList, i):
    vl = QgsVectorLayer("linestring", "Line "+ str(i), "memory")
    vpr = vl.dataProvider()
    vpr.addAttributes([QgsField("Type", QVariant.String)])
    vl.updateFields()
    f = QgsFeature()
    f.setAttributes(["Principal"])
    f.setGeometry(QgsLineString(colectionPointList))
    vpr.addFeature(f)
    vl.updateExtents() 
    QgsProject.instance().addMapLayer(vl)
    
def geraLinhas(verticesRoad, vetVertices, index , path, flag = True):
    pointList = []
    i=0
    if(flag):
        for road in verticesRoad:
            rota = geraVetorDePontos(road.verticesRoad, vetVertices)
            pointList.append(rota)
            # drawLine1(rota,i)
            i= i+1
    else:
        for rlist in verticesRoad:
            for road in rlist:
                rota = geraVetorDePontos(road.verticesRoad, vetVertices)
                pointList.append(rota)
                # drawLine1(rota,i)
                i= i+1

    drawLine(pointList, flag, index, path)

def geraTrilhas(sol: list[SolucaoTrails], area, index, path):
    roads = []
    for ptTrail in sol:
        roads.append(ptTrail.roads)

    geraLinhas(roads, area, index, path, False)