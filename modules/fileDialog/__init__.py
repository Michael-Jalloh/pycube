import pygame as pg
from pycube.components import *
from pycube.core import Application
import time

class App(Application):
    def build(self):
        name = "Socket Server"
        self.l = Label((200, 10), text=name, size=22)
        self.l2 = Label((150, 35), text="Data", size=22)
        btn_info = {'color': TCOLOR, 'onClick': self.go_to_menu, 'width': 40, 'height': 40, 'text': "Quit", 'textColor':WARNING}
        self.b = Button((100, 70), **btn_info)
        slider_info = {"width":100, "height": 20, "color": RED, "backgroundColor": (0,0,0,1), "sliderColor":(200,200,200,100), "onChange": self.sliderHandler}
        self.slider = Slider((200,200), **slider_info)
        #self.container.add_child(self.l)
        #self.container.add_child(self.l2)
        #self.container.add_child(self.b)
        #self.container.add_child(self.slider)
        self.fileDialog = FileDialog((10,10))
        self.container.add_child(self.fileDialog)
        self.last_time = time.time()

    def onStart(self):
        self.fileDialog.hide = False
        rootFolder = self.fileDialog.rootPath
        name = Label((10,10), text=rootFolder, font=Font("roboto_black"), size=20)
        c = Container((0,0), width = WIDTH - 30, height = 25)
        c.add_child(name)
        self.controller.update_bottom_bar(c)

    def sliderHandler(self, sliderPercent):
        self.logger.info(sliderPercent)

    def test(self):
        self.logger.info("Test")

    def go_to_menu(self):
        self.controller.switch_app("menu")

    def quit(self):
        self.controller.quit()
    
    def run(self):
        if pg.K_LEFT in self.events:
            self.slider.add(-1)
        if pg.K_RIGHT in self.events:
            self.slider.add(1)
    
    def controls(self):
        if pg.K_BACKSPACE in self.events:
            rootFolder = self.fileDialog.go_back()
            if rootFolder:
                name = Label((10,10), text=rootFolder, font=Font("roboto_black"), size=20)
                c = Container((0,0), width = WIDTH - 30, height = 25)
                c.add_child(name)
                self.controller.update_bottom_bar(c)
        if pg.K_UP in self.events:
            self.fileDialog.go_up()
        if pg.K_DOWN in self.events:
            self.fileDialog.go_down()
        if (pg.K_RETURN in self.events):# and ((time.time() - self.last_time) > 10):
            self.last_time = time.time()
            rootFolder = self.fileDialog.enter()
            print(rootFolder)
            if rootFolder:
                name = Label((10,10), text=rootFolder, font=Font("roboto_black"), size=20)
                c = Container((0,0), width = WIDTH - 30, height = 25)
                c.add_child(name)
                self.controller.update_bottom_bar(c)

            
