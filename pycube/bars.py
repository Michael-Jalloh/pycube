import psutil as ps
from time import time
from datetime import datetime
from pycube.core import Application
from .components import Container, IconImage, Label, TCOLOR, WIDTH, HEIGHT
from .utils import *

class TopBar(Application):
    def build(self):
        self.container = Container((0,0),width=WIDTH, height=30)
        battery_full = {'name': 'fontawesome', 'icon': 'battery', 'size': 25,
        'color':TCOLOR, 'scale':'auto'}
        bat = IconImage((WIDTH - (100 + 30),10),self.controller.icon, **battery_full)
        self.battery = Label((WIDTH - (170), 10), text="100%", size=16)
        self.date = Label((WIDTH - 90,10), text='20-08-2018', size=16)
        self.time = Label((10,10), text='00:00', size=16)
        bat.position[1] = get_centered_coordinates(bat, self.container)[1] + 2
        self.date.update()
        #self.date.position[1] = get_centered_coordinates(self.date, self.container)[1]
        d, t = str(datetime.now()).split(' ')
        h, s, _ = t.split(':')
        self.date.set_text(d)
        self.time.set_text(h+':'+s)
        bat.update()
        bat.vflip()
        self.container.add_child(bat)
        self.container.add_child(self.battery)
        self.container.add_child(self.date)
        self.container.add_child(self.time)

    def run(self):
        bat = int(ps.sensors_battery().percent) if ps.sensors_battery() else 0
        self.battery.set_text(str(bat)+ '%')
        d, t = str(datetime.utcnow()).split(' ')
        h, s, _ = t.split(':')
        self.date.set_text(d)
        self.time.set_text(h+':'+s)


class BottomBar(Application):
    def build(self):
        self.container = Container((0,HEIGHT - 30),width=WIDTH, height=30)

    def add_child(self, child):
        self.container.clear_children()
        child.position = (0,0)
        self.container.add_child(child)
    
    def clear(self):
        self.container.clear_children()