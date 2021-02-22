import pygame as pg
from pycube.components import *
from pycube.core import Application
from pycube.utils import *

class App(Application):
    def build(self):
        msg = 'TAU'
        k = "Hello World\nFrom Tau\nGlad u could make it"
        talk = MultiLineText((20,100), text=k, width= 100, height=100, padding=5, font=Font("batman_forever"), backgroundColor=(0,0,1))
        l1 = Label((200, 10), text=msg, size=22)
        l2 = Label((200, 40), text=msg, size=22, font=Font("transformer"), color=ERROR)
        l3 = Label((200, 60), text=msg, size=50, font=Font("batman_forever"), color=WARNING)
        icon_info = {'name':'fontawesome','icon':'cube','size':100, 'color':MAGENTA, 'scale':'auto'}
        icon = IconImage((self.container.width / 2, self.container.height /2), self.controller.icon, **icon_info)
        l1.position[0] = get_centered_coordinates(l1, self.container)[0]
        l2.position[0] = get_centered_coordinates(l2, self.container)[0]
        l3.position[0] = get_centered_coordinates(l3, self.container)[0]
        icon.position[0] = get_centered_coordinates(icon, self.container)[0]
        #self.container.add_child(l1)
        #self.container.add_child(l2)
        self.container.add_child(l3)
        self.container.add_child(icon)
        self.name = 'start_screen'
        spinner = Spinner((200,200), width=50, height=50)
        self.container.add_child(spinner)
        self.container.add_child(talk)

    
    def event(self, event):
        if event.type == pg.KEYDOWN:
            self.controller.switch_app('launcher')
