from pycube.components import *
from pycube.core import Application
from pycube.buttonsHandler import ButtonKeys as bkeys
from pycube.eventHandler import Listener, Trigger, EventDispatcher, Event
import pygame as pg

class App(Application):
    def build(self):
        pass

    def onStart(self):
        self.screen = Screen((10,10), width=200, height=200)
        self.screen.add_child(self.setting_screen())
        self.container.add_child(self.screen)
        

    def goto_setting(self, event):
        self.screen.add_child(self.setting_screen())
    
    def goto_about(self, event):
        self.screen.add_child(self.about_screen())


    def setting_screen(self):
        d = EventDispatcher()
        setting_event = Event(bkeys.B, self.goto_about)
        setting_listener = Listener(d, setting_event)
        sTrigger = Trigger(d, setting_event)
        container = ContainerEvent(width=200, height=200, triggers = [sTrigger])
        vscroll = VScrollView(width=200, height=200)
        l = Label((10,10),text="About")
        vscroll.add_child(l)
        container.add_child(vscroll)
        return container
    
    def about_screen(self):
        d = EventDispatcher()
        about_event = Event(bkeys.B, self.goto_setting)
        about_listener = Listener(d, about_event)
        aTrigger = Trigger(d, about_event)
        container = ContainerEvent(width=200, height=200, triggers = [aTrigger])
        vscroll = VScrollView(width=200, height=200, border=2, borderColor=(255,255,255))
        msg = "This is the Tau\nIts your personal terminal\nFeatures:\n--------------\n* Run python scripts\n* Run retropie\n* Run Steamlink"
        l = MultiLineText((10,10),width = 200, height = 200, text=msg)
        vscroll.add_child(l)
        container.add_child(vscroll)
        return container

    def controls(self):
        self.screen.events(self.bsp)