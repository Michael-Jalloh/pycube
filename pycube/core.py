from datetime import datetime
from .components import *
from .settings import *
from .tasker import Task

class Application(object):
    def __init__(self,controller):
        self.name = ""
        self.logger : Logger = Logger()
        self.icon = ""
        self.tasker : Task = Task()
        self.controller = controller
        self.container : Container = Container((0, 30), backgroundColor= BGCOLOR, width= WIDTH - 1, height= HEIGHT - 61, border= 3)
        self.events = set()
        self.bsp = []
        self.analog = []
        self.keyboard : Keyboard = None
        self.build()

    def build(self):
        pass

    def run(self):
        pass

    def update(self):
        self.container.update(self.controller.screen)

    def draw(self):
        self.container.draw(self.controller.screen)

    def draw_keyboard(self):
        if self.keyboard and self.keyboard.active:
            self.keyboard.draw(self.controller.screen)

    def event(self, event):
        if event.type == pg.KEYDOWN:
            self.events.add(event.key)
        elif event.type == pg.KEYUP:
            self.events.discard(event.key)
        self.controls()

    def gamepad(self, events):
        self.bsp, self.analog = events

    def controls(self):
        pass

    def onStart(self):
        pass

    def onExit(self):
        pass

class Logger(object):

    def info(self, message):
        print(f"[INFO] -> {datetime.utcnow()} -> {message}")
    
    def warning(self, message):
        print(f"[WARNING] -> {datetime.utcnow()} -> {message}")
    
    def error(self, message):
        print(f"[ERROR] -> {datetime.utcnow()} -> {message}")
    
    def danger(self, message):
        print(f"[DANGER] -> {datetime.utcnow()} -> {message}")