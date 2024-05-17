# -*- coding: utf-8 -*-
"""
/***************************************************************************
 alocacaoOtimizada
                                 A QGIS plugin
 Alocação Otimizada de Pátios
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-05-24
        copyright            : (C) 2022 by Alexandre Breda
        email                : alexandre.breda@edu.ufes.br
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load alocacaoOtimizada class from file alocacaoOtimizada.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    #from .alocacao_otimizada import alocacaoOtimizada
    from .alocacao_otimizada import alocacao_otimizada
    #return alocacaoOtimizada(iface)
    return alocacao_otimizada(iface)
