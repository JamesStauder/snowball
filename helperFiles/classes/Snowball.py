import pyqtgraph as pg
import pyqtgraph.exporters
import h5py
import numpy as np

from ..constants import *

class Snowball():
    def __init__(self):
        print("Snowball Init")
        #self.data = datasetDict

    # TODO: seperate into seperate functions
    # TODO: Does not need to be done in the black box
    def createImage(self, name):
        print ("Creating image")
        # generate something to export
        # plt = pg.plot([1,5,2,4,3])

        colorMapFile = h5py.File(cmFileName, 'r')
        self.colorData = colorMapFile[name][:]
        colorMapFile.close()

        
        plotData = np.flip(np.rot90(np.array(self.colorData)[::10,::10]),0)
        
        plt = pg.ImageItem(plotData)
        # plt.scale(.5,.5)
        plt.save('./cache/fileName.png')
        # create an exporter instance, as an argument give it
        # the item you wish to export
        # exporter = pg.exporters.ImageExporter(plt.plotItem)
        
        # set export parameters if needed
        # exporter.parameters()['width'] = 100.0   # (note this also affects height parameter)
        
        # save to file
        # exporter.export('./cache/fileName.png')