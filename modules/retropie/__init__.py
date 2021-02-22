import os, time
from pycube.components import *
from pycube.core import Application

class App(Application):
    def onStart(self):
        l = Label((0,0), text="Launching Retropie", size=30)
        l.position = get_centered_coordinates(l, self.container)
        self.container.add_child(l)
        self.last_check = time.time()

    def run(self):
        if (time.time() - self.last_check) > 5:
            var = os.popen("emulationstation")
            self.controller.switch_app("launcher")