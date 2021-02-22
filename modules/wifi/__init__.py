import pygame as pg
from wifi import Cell, Scheme
from pycube.components import *
from pycube.core import Application

class App(Application):
    def build(self):
        pass

    def onStart(self):
        self.cells = Cell.all('wlo1')
        self.cells_holder = {}
        self.c = VScrollView((10,10),width=SCREEN_WIDTH, height=SCREEN_HEIGHT, border=2, borderColor=(255,255,255))
        for index, cell in enumerate(self.cells):
            l = Label((0,0), text=f" {cell.ssid} ", backgroundColor=(255,255,255), size=30, border=2, borderColor=(255,255,255), padding=10, onClick=self.pick_cell, onClickData=cell.ssid)
            self.c.add_child(l)
            self.cells_holder[cell.ssid] = cell
        self.container.add_child(self.c)

    def pick_cell(self, *cell):
        print("Cell")
        print(self.cells_holder["".join(cell)].ssid)

    def controls(self):
        if(pg.K_UP in self.events):
            self.c.prev()
        elif(pg.K_DOWN in self.events):
            self.c.next()
        elif pg.K_RETURN in self.events:
            self.c.selected_child().click()
        for child in self.c.childComponents:
            child.border = 0
        self.c.selected_child().border=3