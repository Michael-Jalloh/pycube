from ipwebcam import IPWEBCAM
from pycube.components import *
from pycube.core import Application
import pygame as pg 

class App(Application):
    def onStart(self):
        self.ipcam = IPWEBCAM(height=240, width=460)
        self.img = Image((10,10), width=200, height=200, image=self.ipcam.get_pygame_image())
        self.container.add_child(self.img)

    def run(self):
        self.img.set_pygame_img(self.ipcam.get_pygame_image())