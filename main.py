import time
import pygame as pg
from importlib import import_module
from pycube.utils import *
from pycube.settings import *
from pycube.components import *
import pycube.bars
from pycube.buttonsHandler import ButtonsHandler
from pycube.buttonsHandler import ButtonKeys as bkeys
import os, traceback

class PyCude(object):
    def __init__(self):
        # Initialize game window, etc
        self.orientation = 0 # 0 for portrait, 1 for landscape
        self.FPS = 30
        self.width = WIDTH
        self.height = HEIGHT
        pg.init()
        self.screen = pg.display.set_mode((self.width, self.height), pg.HWACCEL | pg.NOFRAME, 32)
        pg.display.set_caption("PyCube")
        self.screen.fill(BGCOLOR)
        pg.display.flip()
        self.clock = pg.time.Clock()
        self.running = True
        self.icon = Icons()
        self.buttonsHandler = ButtonsHandler()
        self.apps = {}
        self.top_bar = pycube.bars.TopBar(self)
        self.bottom_bar = pycube.bars.BottomBar(self)
        self.setup()
        self.current_app = 'launcher'
        
    def update_bottom_bar(self, child):
        self.bottom_bar.add_child(child)
    
    def clear_bottom_bar(self):
        self.bottom_bar.clear()

    def setup(self):
        # Setup apps to run
        self.apps = {}
        dirs = [path for path in os.listdir('modules') if os.path.isdir(os.path.join('modules',path))]
        dirs.sort()
        for directory in dirs:
            try:
                if(directory == "__pycache__"):
                    continue
                module = __import__('modules.' + directory)
                app = getattr(module, directory)
                self.apps[directory] = app.App(self)
                self.apps[directory].name = directory
                self.apps[directory].icon = os.path.join(".","modules",directory,"logo.png")
            except Exception as e:
                traceback.print_exc()
                pass


    def run(self):
        # App loop
        self.start_screen()
        self.switch_app("launcher")
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.currentApp().run()
            self.top_bar.run()
            self.bottom_bar.run()
            self.update()
            self.draw()
        self.end_screen()


    def update(self):
        # App loop - update
        self.screen.fill(BGCOLOR)
        self.currentApp().update()
        self.top_bar.update()
        self.bottom_bar.update()

    def events(self):
        # App loop - events
        gamepad = self.buttonsHandler.get()
        if (bkeys.START in gamepad[0]) and (bkeys.SELECT in gamepad[0]):
            if self.currentApp().name != "launcher":
                self.switch_app("launcher")
            return
        if self.currentApp().keyboard and self.currentApp().keyboard.active:
            self.currentApp().keyboard.get_events(gamepad)
        else:  
            self.currentApp().gamepad(gamepad)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                return
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                if self.currentApp().name != "launcher":
                    self.switch_app("launcher")
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.currentApp().keyboard and self.currentApp().keyboard.active:
                    self.currentApp().keyboard.get_clicked_child(event)
                else:
                    child = self.currentApp().container.get_clicked_child(event)
                    if child:
                        child.on_click()
            else:
                if self.currentApp().keyboard and self.currentApp().keyboard.active:
                    self.currentApp().keyboard.event(event)
                else:
                    self.currentApp().event(event)
            
    def draw(self):
        # App loop - draw
        self.currentApp().draw()
        self.currentApp().draw_keyboard()
        self.top_bar.draw()
        self.bottom_bar.draw()
        pg.display.flip()

    def start_screen(self):
        # Start screen
        self.screen.fill(BGCOLOR)
        font = Font("batman_forever")
        font.draw_text(self.screen, "Tau",  WIDTH / 2, 20, size=30)
        icon = self.icon.get_icon('fontawesome','cube', 100, color=TCOLOR)
        rect = icon.get_rect()
        coordinates = get_centered_coordinates(rect, self.screen.get_rect())
        rect.x = coordinates[0]
        rect.y = coordinates[1]
        self.screen.blit(icon,rect)
        pg.display.flip()
        self.wait_time_pass(0)

    
    def end_screen(self):
        # End screen
        self.screen.fill(BGCOLOR)
        font = Font('lobster')
        msg = "Shutting down"
        font.draw_text(self.screen, msg,  WIDTH / 2, 20, size=22)
        icon = self.icon.get_icon('fontawesome','cube', 100, color=TCOLOR)
        rect = icon.get_rect()
        coordinates = get_centered_coordinates(rect, self.screen.get_rect())
        rect.x = coordinates[0]
        rect.y = coordinates[1]
        self.screen.blit(icon,rect)
        pg.display.flip()
        print (msg)
        self.wait_time_pass(2)

    def currentApp(self):
        return self.apps[self.current_app]

    def wait_key_press(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    waiting = False
        #    self.top_bar.update()
        #    self.top_bar.draw()

    def wait_time_pass(self, wait_time=20):
        '''Wait_time is the amount of time that the function
           should wait before it exits. the time is in seconds
           defualt = 20'''
        start_time = time.time()
        timed = time.time() - start_time
        while (timed < wait_time):
            timed = time.time() - start_time
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    waiting = False

    def quit(self):
        self.running = False

    def switch_app(self, app):
        try:
            if self.apps.get(app, None) != None:
                self.currentApp().onExit()
                self.currentApp().events = set()
                self.clear_bottom_bar()
                self.current_app = app
                self.currentApp().onStart()
        except Exception:
            traceback.print_exc()
            self.current_app = "launcher"

# Start application
app = PyCude()
app.run()

pg.quit()
