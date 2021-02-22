from pycube.components import *
from pycube.core import Application
import pygame as pg

class App(Application):
    def onStart(self):
        msg = Label((10,10), text="Create logos from fontawesome icons", size=20) #, font=fonts["roboto"])
        self.vbox = VScrollView((10,40), width = 250, height = 200, border=2, borderColor=BLUE)
        self.container.add_child(msg)
        self.container.add_child(self.vbox)
        self.icons = Icons()
        with open("icon.txt") as f:
            for icon in f.readlines():
                l = Label((10,0), text=icon.strip("\n"), padding=5, onClick=self.iconSelect, onClickData=icon.strip("\n"))
                self.vbox.add_child(l)
    
    def run(self):
        if(pg.K_UP in self.events):
            self.vbox.prev()
        elif(pg.K_DOWN in self.events):
            self.vbox.next()
        for child in self.vbox.childComponents:
            child.border = 0
        self.vbox.selected_child().border=3
        if(pg.K_KP_ENTER in self.events or pg.K_RETURN in self.events):
            self.vbox.selected_child().click()
        
    def iconSelect(self, *icon):
        icon = "".join(icon)
        self.logger.info(icon)
        self.icons.icons["fontawesome"].export_icon(icon, 100, color=TCOLOR)
        