# -*- coding: utf-8 -*-
"""
/***************************************************************************
 alocacaoOtimizada
                                 A QGIS plugin
 Alocação Otimizada de Pátios
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2022-05-24
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Alexandre Breda
        email                : alexandre.breda@edu.ufes.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt import QtWidgets
from qgis.core import QgsProject

# Initialize Qt resources from file resources.py
from .resources import *

from .alocacao_otimizada_dialog import alocacaoOtimizadaDialog
from .road_screen2_dialog import interface
import os.path

import math # sqrt, pow
from random import seed, randint # seed, randomint
from datetime import datetime # datetime
import sys # maxint
import time # time

from .Services.PreProcLayer import PreProcLayer
from .Heuristicas import Heuristicas
from .SA import SA
from .Services.Draw import geraPontosMemoy, geraLinhas, geraTrilhas, geraPontosPatiosMarcelo, geraFilePontos
from .Models.Grafo import Grafo
from .roadsAprovTrecho import RoadsAprovTrecho
from .Models.SolucaoRoad import AccessRoad
from .Models.SolucaoStorageYard import SolucaoStorageYard
from .ExecutarTrilhas import ExecutarTrilhas
from .Services.commons import marcaArvoresPatios, quantidadeArvoresPatio
from .Exceptions.LayerException import LayerException, MultipleLayerException
from .Exceptions.SimulatedAnnealingException import SimulatedAnnealingException, MultipleSimulatedAnnealingExceptionException 

seed(1)

class alocacao_otimizada:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'alocacaoOtimizada_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Alocação Otimizada de Pátios')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('alocacaoOtimizada', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/alocacao_otimizada/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'AlocaçãoOtimizada'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Alocação Otimizada de Pátios'),
                action)
            self.iface.removeToolBarIcon(action)

    def runProcStorageYard(self, layers, dlg):
        multipleExceptions = MultipleLayerException()

        verticesIndex = dlg.cmb_vertices.currentIndex()
        if(verticesIndex != 0):
            camadaVertices = layers[verticesIndex - 1].layer()
        else:
            multipleExceptions.exceptions.append(LayerException("verticeLayer"))

        patiosIndex = dlg.cmb_patios.currentIndex()
        if(patiosIndex != 0):
            camadaPatio = layers[patiosIndex - 1].layer()
        else:
            multipleExceptions.exceptions.append(LayerException("patioLayer"))

        floresta_expIndex = dlg.cmb_arvExp.currentIndex()
        if(floresta_expIndex != 0):
            camadaFloresta_exp = layers[floresta_expIndex - 1].layer()
        else:
            multipleExceptions.exceptions.append(LayerException("FlorestaLayer"))

        inclinacaoIndex = dlg.cmb_inclinacao.currentIndex()
        if(inclinacaoIndex != 0):
            camadaInclinacao = layers[inclinacaoIndex - 1].layer()
        else:
            multipleExceptions.exceptions.append(LayerException("InclinacaoLayer"))
        
        if(len(multipleExceptions.exceptions) > 0):
            QtWidgets.QMessageBox.critical(dlg, "Error", multipleExceptions.__str__())
            return
        
        dicionario = {}
        inundacaoIndex = dlg.cmb_inundacao.currentIndex()
        if(inundacaoIndex != 0):
            camadaInundacao = layers[inundacaoIndex - 1].layer()
            dicionario["inundacao"] = True
        else:
            dicionario["inundacao"] = False

        appIndex = dlg.cmb_app.currentIndex()
        if(appIndex != 0):
            camadaApp = layers[appIndex - 1].layer()
            dicionario["app"] = True
        else:
            dicionario["app"] = False

        arvoreRemanescenteIndex = dlg.cmb_arvoresRemanescentes.currentIndex()
        if(arvoreRemanescenteIndex != 0):
            camadaArvoreRemanescente = layers[arvoreRemanescenteIndex - 1].layer()
            dicionario["arvoresRemanescente"] = True
        else:
            dicionario["arvoresRemanescente"] = False

        # ----------------Heurística-----------------

        DISTANCIA_MAXIMA = float(dlg.lineEditDistArvorePatio.text())

        NUM_PATIOS = int(dlg.lineEditNumeroPatios.text())

        FLEXSUP = float(dlg.lineEditFlexSup.text())
        FLEXSUP = FLEXSUP / 100

        NUM_ITERACOES = int(dlg.lineEditNUM_ITERACOES.text())

        NUM_ROADS = NUM_PATIOS + 1

        NUM_ARV_TRILHA = 15

        PENALIZACAO_VOLUME = 1000

        NUM_VERTICES = int(camadaVertices.featureCount())

        NUM_VERTICES_PATIOS = int(camadaPatio.featureCount())

        NUM_ARVORES_EXPLORAVEIS = int(camadaFloresta_exp.featureCount())

        # ---------------- SA -----------------

        useSimulatedAnnealing = dlg.SA.isChecked()

        if(useSimulatedAnnealing):
            SAExceptions = []

            try:
                TAXARESFRIAMENTO_YARD = float(dlg.lineEditTaxaResfriamento.text())
            except:
                SAExceptions.append("Taxa de resfriamento E invalida")
            
            try:
                ITERACOESVIZINHANCA_YARD = float(dlg.lineEditIteracoesVizinhanca.text())
            except:
                SAExceptions.append("Iteracoes de vizinhanca E invalida")    
            
            try:
                TEMPERATURAINICIAL_YARD = float(dlg.lineEditTemperaturaInicial.text())
            except:
                SAExceptions.append("Temperatura inicial E invalida")

            try:
                TEMPERATURACONGELAMENTO_YARD = float(dlg.lineEditTemperaturaCongelamento.text())
            except:                
                SAExceptions.append("Temperatura de congelamento E invalida")

            if(len(SAExceptions) > 0):
                message = "\n".join(SAExceptions)
                QtWidgets.QMessageBox.critical(dlg, "Erro no SA", message)
                return

        #--------------------- Tempos -----------------

        TEMPOEXEC = 12 * 60 * 60

        #--------------- Pré Processamento -----------------
        preProcLayer = PreProcLayer(NUM_VERTICES)

        area = preProcLayer.lerInstanciaVertices(camadaVertices)

        patios = preProcLayer.lerInstanciaPatiosDadosMarcelo(camadaPatio, area)

        arvoresExploraveis = preProcLayer.lerInstanciaArvoresExploraveis(camadaFloresta_exp)

        inclinacao = preProcLayer.lerInstanciaInclinacao(camadaInclinacao)

        if(dicionario["arvoresRemanescente"]):
            desvios = preProcLayer.lerInstanciaArvoresRemanescentes(camadaArvoreRemanescente)
        else:
            desvios = None

        if(dicionario["inundacao"]):
            inuncao = preProcLayer.lerInstanciaInundacao(camadaInundacao)
        else:
            inuncao = None
        
        if(dicionario["app"]):
            app = preProcLayer.lerInstanciaAPP(camadaApp)
        else:
            app = None

        # Pega o mock dos valores de distancia
        distanciasPatArv = preProcLayer.lerArquivoDistancias()

        volumeTot = preProcLayer.calculaVolume(arvoresExploraveis, NUM_ARVORES_EXPLORAVEIS)

        restVolSup = (volumeTot / NUM_PATIOS) * (1 + FLEXSUP)

        #-----Inicio do programa-------

        heuristica = Heuristicas(NUM_PATIOS, NUM_ARVORES_EXPLORAVEIS, DISTANCIA_MAXIMA, NUM_VERTICES_PATIOS, PENALIZACAO_VOLUME)

        # newSolucao: SolucaoStorageYard = SolucaoStorageYard()
        # newSolucao.patios = [667, 526, 1280, 921, 294, 496, 1358, 63, 1483, 177, 638, 1525, 1042, 308]
        # # # # [537, 268, 1344, 1065, 1405, 750, 1494, 415, 291, 304, 1373, 950, 720, 173]
        # # # # [547, 273, 1358, 949, 1434, 812, 1525, 370, 296, 309, 1414, 969, 735, 176]
        # # # # [1525, 1434, 1401, 1086, 1371, 969, 734, 547, 296, 423, 273, 176, 764, 257]

        # newSolucao = heuristica.calculaFOPatio(arvoresExploraveis, distanciasPatArv, newSolucao, restVolSup)

        # #---------------DEFININDO GRAFO-----------------

        # grafo = Grafo()
        # grafo.cria_Grafo(NUM_VERTICES, 8, 1)
        # grafo.insereArestaArea(area, desvios, inuncao, app, inclinacao)

        # # -------------- ROADS -------------
        
        # NUM_ACCESS_ROAD = 1
        # estradaDeAcesso = AccessRoad()
        # solRoad_aux = RoadsAprovTrecho()
        # estradaDeAcesso.inicio.append(1)
        # solRoad = solRoad_aux.roadsAprovTrecho(grafo, area, patios, newSolucao, estradaDeAcesso, NUM_PATIOS, NUM_VERTICES, NUM_ACCESS_ROAD)

        # # -------------- TRAILS -------------
        # arvoreSelPatios = marcaArvoresPatios(newSolucao, distanciasPatArv, NUM_ARVORES_EXPLORAVEIS, NUM_PATIOS)
        # quantidadeArvores = quantidadeArvoresPatio(arvoreSelPatios, NUM_PATIOS, NUM_ARVORES_EXPLORAVEIS)
        # trilha = ExecutarTrilhas()
        # solTrilha = trilha.trails( area, solRoad, patios, newSolucao, arvoresExploraveis, arvoreSelPatios, distanciasPatArv, app, quantidadeArvores, restVolSup, desvios, NUM_VERTICES, NUM_PATIOS, NUM_ROADS, NUM_ARVORES_EXPLORAVEIS, NUM_ARV_TRILHA)

        # # newSolucao.fileWritter(0, restVolSup)
        # # geraPontosMemoy(newSolucao, camadaPatio, 0)
        # # geraPontosPatiosMarcelo(newSolucao, camadaPatio, 0)
        # # for j in range(len(newSolucao.arvores)):
        # #     geraPontosArvores(newSolucao.arvores[j], arvoresExploraveis, newSolucao.patios[j], 0)
        # # geraLinhas(solRoad.roads, area) #Aqui esta desenhando a linha do ponto inicial ate o ponto final
        # # geraTrilhas(solTrilha, area)

        for i in range(1):
            #---------------DEFININDO NUMERO DE ACESSOS-----------------    
            estradaDeAcesso = getAccesPoints(dlg)
            NUM_ACCESS_ROAD = len(estradaDeAcesso.inicio)

            if(NUM_ACCESS_ROAD == 0):
                QtWidgets.QMessageBox.warning(dlg, "Sem acessos", "Por favor, insira pelo menos um acesso.")
                return

            solPatios = SolucaoStorageYard()
            solPatios = heuristica.heuConstrutivaIter(arvoresExploraveis, distanciasPatArv, NUM_ITERACOES, restVolSup)

            if useSimulatedAnnealing == True:
                sa = SA(NUM_PATIOS, NUM_ARVORES_EXPLORAVEIS, DISTANCIA_MAXIMA, NUM_VERTICES_PATIOS, PENALIZACAO_VOLUME, TEMPOEXEC)
                solPatios = sa.SAStorageYard(arvoresExploraveis, distanciasPatArv, solPatios, restVolSup, TAXARESFRIAMENTO_YARD, ITERACOESVIZINHANCA_YARD, TEMPERATURAINICIAL_YARD, TEMPERATURACONGELAMENTO_YARD)

            #---------------DEFININDO GRAFO-----------------
            grafo = Grafo()
            grafo.cria_Grafo(NUM_VERTICES, 8, 1)
            grafo.insereArestaArea(area, desvios, inuncao, app, inclinacao)

            # -------------- ROADS -------------
            solRoad_aux = RoadsAprovTrecho()
            solRoad = solRoad_aux.roadsAprovTrecho(grafo, area, patios, solPatios, estradaDeAcesso, NUM_PATIOS, NUM_VERTICES, NUM_ACCESS_ROAD)

            # -------------- TRAILS -------------
            arvoreSelPatios = marcaArvoresPatios(solPatios, distanciasPatArv, NUM_ARVORES_EXPLORAVEIS, NUM_PATIOS)
            quantidadeArvores = quantidadeArvoresPatio(arvoreSelPatios, NUM_PATIOS, NUM_ARVORES_EXPLORAVEIS)
            trilha = ExecutarTrilhas()
            solTrilha = trilha.trails( area, solRoad, patios, solPatios, arvoresExploraveis, arvoreSelPatios, distanciasPatArv, app, quantidadeArvores, restVolSup, desvios, NUM_VERTICES, NUM_PATIOS, NUM_ROADS, NUM_ARVORES_EXPLORAVEIS, NUM_ARV_TRILHA)

            # solPatios.fileWritter(i, restVolSup)

            geraLinhas(solRoad.roads, area) #Aqui esta desenhando a linha do ponto inicial ate o ponto final
            geraPontosPatiosMarcelo(solPatios, camadaPatio, i)
            geraTrilhas(solTrilha, area)
            #TODO: esta com problema aqui
            # geraTrilhas(solucaoTrilha, area)
            # for j in range(len(solPatios.arvores)):
            #     geraPontosArvores(solPatios.arvores[j], arvoresExploraveis, solPatios.patios[j], i)

        QtWidgets.QMessageBox.information(dlg, "Success", "Terminou a execucao!")

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = interface()

        layers = QgsProject.instance().layerTreeRoot().children()

        # self.dlg.comboBoxAPP.clear()
        # self.dlg.comboBoxAPP.addItems([layers.name() for layers in layers])
        self.dlg.cmb_vertices.clear()
        self.dlg.cmb_vertices.addItem('None') 
        self.dlg.cmb_vertices.addItems([layers.name() for layers in layers])

        self.dlg.cmb_patios.clear() 
        self.dlg.cmb_patios.addItem("None")
        self.dlg.cmb_patios.addItems([layers.name() for layers in layers])
        
        self.dlg.cmb_arvExp.clear()
        self.dlg.cmb_arvExp.addItem("None")
        self.dlg.cmb_arvExp.addItems([layers.name() for layers in layers])
        
        self.dlg.cmb_inundacao.clear()
        self.dlg.cmb_inundacao.addItem("None")
        self.dlg.cmb_inundacao.addItems([layers.name() for layers in layers])
        
        self.dlg.cmb_app.clear()
        self.dlg.cmb_app.addItem("None")
        self.dlg.cmb_app.addItems([layers.name() for layers in layers])
        
        self.dlg.cmb_inclinacao.clear()
        self.dlg.cmb_inclinacao.addItem("None")
        self.dlg.cmb_inclinacao.addItems([layers.name() for layers in layers])
        
        self.dlg.cmb_arvoresRemanescentes.clear()
        self.dlg.cmb_arvoresRemanescentes.addItem("None")
        self.dlg.cmb_arvoresRemanescentes.addItems([layers.name() for layers in layers])

        # self.dlg.doubleSpinBoxDistArvorePatio.clear()
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # sol = SolucaoStorageYard()
            # print(sol.__str__())
            self.runProcStorageYard(layers, self.dlg)

def getAccesPoints(dialog) -> AccessRoad:
        acessPoints = AccessRoad()
        for i in range(dialog.accesPointsTable.rowCount()):
            acessPoints.inicio.append(int(dialog.accesPointsTable.item(i, 0).text()) - 1)
        return acessPoints
