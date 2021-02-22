import pygame as pg
from pycube.components import *
from pycube.core import Application

class App(Application):
    def onStart(self):
        self.controller.quit()