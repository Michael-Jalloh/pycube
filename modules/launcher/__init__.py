from pycube.components import *
from pycube.core import Application
from pycube.buttonsHandler import ButtonKeys as bkeys

import pygame as pg

class App(Application):
    def build(self):
        pass

    def change_app(self, *app_name):
        app_name = ''.join(app_name)
        self.controller.switch_app(app_name)
    
    def onStart(self):
        name = Label((10,10), text="Launcher", font=Font("roboto_black"), size=25)
        c = Container((0,0), width = WIDTH - 30, height = 25)
        c.add_child(name)
        self.controller.update_bottom_bar(c)
        icon_info = {'name':'fontawesome', 'icon':'apple', 'size':100, 'color':TCOLOR, 'scale': 'auto', 'onClick': self.quit}
        icon = Icons()
        heading_info = {"text":"Menu", "size": 50}
        self.circle = CircleContainer((100,100), radius = 80, onClick=self.toogle, thickness=3)
        heading = Label((50, 50), **heading_info)
        self.i = IconImage((10,10),icon, **icon_info)
        self.circle.set_content(self.i)
        self.c = HScrollView((10,10),width=self.container.width - 20, height = self.container.height - 20)
        self.circle.position = get_centered_coordinates(self.circle, self.c)
        #self.c.add_child(self.circle)
        self.container.add_child(heading)
        self.container.add_child(self.c)
        self.app_list = []
        self.current_app = 0
        self.apps = {}
        x = 10
        for app in self.controller.apps:
            if (app == "start_screen"):
                continue
            i = Image((0,0), width=80,height=80, path=self.controller.apps[app].icon)
            cc = CircleContainer((0,0),radius = 60, onClick=self.change_app, onClickData=app, thickness=3 )
            ##cc = HexContainer((0,0), 60, color=(0,0,0), orientation=2, border=4)
            cc.set_content(i)
            l = Label((10,130), text=app.capitalize(), size=20)
            c = Container((100,100), width=150,height=155, onClick=self.change_app, onClickData=app)
            #c.position[1] = get_centered_coordinates(c, self.c)[1]
            #c.position[0] = x
            l.position[0] = get_centered_coordinates(l, c)[0]
            c.add_child(cc)
            c.add_child(l)
            self.app_list.append(app)
            self.apps[app] = c
            x += 150
            self.c.add_child(c)

    def quit(self):
        self.controller.quit()
    
    def toogle(self, *app_name):
        #pg.image.save(self.i.surface, "apple.png")
        app_name = "".join(app_name)
        self.apps[app_name].get_child(0).toggle()
    
    def controls(self):
        if (pg.K_LEFT in self.events) or (bkeys.LEFT in self.bsp):
           self.c.prev() #_child()
        if (pg.K_RIGHT in self.events) or (bkeys.RIGHT in self.bsp):
            self.c.next() #_child()
        if (pg.K_RETURN in self.events) or (bkeys.B in self.bsp):
            self.c.selected_child().on_click()
        for c in self.c.childComponents:
            if c.get_child(0).is_activated == False:
                c.get_child(0).toggle()
                c.position[1] = get_centered_coordinates(c, self.c)[1]
        if (self.c.selected_child().get_child(0).is_activated == True):
            self.c.selected_child().get_child(0).toggle()
            self.c.selected_child().position[1] = 25 
    