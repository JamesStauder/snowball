##################################
#Creator: James Stauder
#Creation Date: 1/30/18
#Last edit Date: 2/05/18
#Purpose: Class to make Dataset objects
#Parameters: 
#name -> name of dataset
#pen -> color of pen to use in plotting
#Attributes:
#name -> name of dataset
#pen -> color of pen to use in plotting
#interp -> interpolator based 
#
#
##################################

from __future__ import division, print_function
import time
import sys
import h5py
import numpy as np
import pyqtgraph as pg
import fenics as fc
import dolfin as df

from scipy.interpolate import RectBivariateSpline
import matplotlib
matplotlib.use('Agg')
from pylab import sqrt, linspace
from ..constants import *
from ..createColorTiles import *

class Dataset():
    def __init__(self, name, pen):
        self.name = name
        self.pen = pen


        #TODO can these be changed to globals? Takes no time to do but it is done on repeat
        bed_xarray = linspace(map['proj_x0'], map['proj_x1'], map['x1'], endpoint=True)
        bed_yarray = linspace(map['proj_y1'], map['proj_y0'], map['y1'], endpoint=True)


        if self.name == 'velocity':
            self.data, self.vx, self.vy = self.setData(name)
            self.vxInterp = RectBivariateSpline(bed_xarray, bed_yarray, np.flipud(self.vx).transpose())
            self.vyInterp = RectBivariateSpline(bed_xarray, bed_yarray, np.flipud(self.vy).transpose())

        else:
            self.data = self.setData(name)

        self.interp   = RectBivariateSpline(bed_xarray, bed_yarray, np.flipud(self.data).transpose())

        #Only create color map if we wish to render possible in the future where we wish to create Dataset for backend web
        #if render and name != 'VX' and name != 'VY':
        #    createColorMap(self)
        #    self.pathPlotItem = pg.PlotDataItem([0,0], pen=self.pen)
        self.createColorMap()


    def setData(self, name):
        dataFile = h5py.File(dataFileName, 'r')
        if name == 'velocity':
            vx = dataFile['VX'][:]
            vy = dataFile['VY'][:]
            data = sqrt(vx**2 + vy**2)
            dataFile.close()
            return data, vx, vy
        else:
            data = dataFile[name][:]
            dataFile.close()
            return data

    def getInterpolatedValue(self, xPosition, yPosition):
        return self.interp(xPosition, yPosition)

    def createColorMap(self):
        colorMapFile = h5py.File(cmFileName, 'r')
        self.colorData = colorMapFile[self.name][:]
            
        # self.imageItem = pg.ImageItem(self.colorData)
        # self.imageItem.setOpts(axisOrder='row-major')

        # self.plotWidget = pg.PlotWidget()
        # self.plotWidget.addItem(self.imageItem)
        # self.plotWidget.setAspectLocked(True)
        # self.plotWidget.invertY(True)

        # self.colorMap = getCM(self.name)
        # self.colorBar = getColorBar(self.name, self.colorMap)

        '''Commented out because it is broken. line that breaks it ->    self.colorBarAnchorWidget.setParentItem(self.plotWidget.getPlotItem())
        self.colorBarAnchorWidget = ColorBarAnchorWidget()
        self.colorBarAnchorWidget.hideAxis('left')
        self.colorBarAnchorWidget.hideAxis('bottom')
        self.colorBarAnchorWidget.addItem(self.colorBar)
        


        self.plotWidget.addItem(self.colorBarAnchorWidget)

        self.colorBarAnchorWidget.setFixedWidth(158)
        self.colorBarAnchorWidget.setFixedHeight(250)
        self.colorBarAnchorWidget.setAspectLocked(True)

        self.colorBarAnchorWidget.getViewBox().setRange(xRange=[-64.0, 114], yRange=[-15,247], padding=0.0)
        self.colorBarAnchorWidget.invertY(True)

        self.colorBarAnchorWidget.setParentItem(self.plotWidget.getPlotItem())
            
        self.colorBarAnchorWidget.getViewBox().setMouseEnabled(x=False, y=False)
        self.colorBarAnchorWidget.anchor(itemPos=(1,0), parentPos=(1,0), offset=(-10,-10))
       
        '''
        colorMapFile.close()

        
