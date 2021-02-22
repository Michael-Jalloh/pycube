import os, time
from pycube.components import Label
from pycube.core import Application
from pycube.utils import get_centered_coordinates

class App(Application):

    def onStart(self):
        l = Label((0,0), text="Launching SteamLink", size=30)
        l.position = get_centered_coordinates(l, self.container)
        self.container.add_child(l)
        self.last_check = time.time()
    
    def run(self):
        if (time.time() - self.last_check) > 5:
            var = os.popen("steamlink")
            self.controller.switch_app("launcher")