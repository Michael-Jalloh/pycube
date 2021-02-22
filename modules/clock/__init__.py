from datetime import datetime
import pygame as pg
from pycube.components import *
from pycube.core import Application
from .logo import make_logo

class App(Application):
    def build(self):
        self.time = Label((100,100), text="Clock", size=50, font=Font("transformer"))
        self.date = Label((0,175), text="Date", size=30, font=Font("transformer"))
        self.time.position = get_centered_coordinates(self.time,self.container)
        self.date.position[0] = get_centered_coordinates(self.date, self.container)[0] 
        self.time.position[0] -= self.time.width/4
        self.date.position[0] -= self.date.width/2
        self.btn = Button((10,10), text="Test", onClick=self.make_logo)
        self.container.add_child(self.time)
        self.container.add_child(self.date)
        self.container.add_child(self.btn)
        self.textEntry = TextEntryField((50, 20),self, "", width=100, height=20)
        self.textEntry2 = TextEntryField((50, 50),self, "", width=100, height=20)
        self.container.add_child(self.textEntry)
        self.container.add_child(self.textEntry2)
        self.job_id = None
        self.rotation = 0
        self.spinner = Spinner((200,200), width=50, height=50)
    
    def onStart(self):
        pass
        #self.job_id = self.tasker.add_job(add_module).get_id()
        #self.logger.info(self.job_id)

    def run(self):
        d,t = str(datetime.utcnow()).split(" ")
        t,_ = t.split(".")
        self.time.set_text(f"{t}")
        self.date.set_text(f"{d}")
        if self.job_id:
            try:
                job = self.tasker.get_job(self.job_id)
                if job.is_finished:
                    self.logger.info("Job Done...")
                    self.container.remove_child(self.spinner)
                else:
                    self.logger.info("Job in process")
            except:
                self.job_id = None
                
    def controls(self):
        if pg.K_ESCAPE in self.events:
            self.controller.switch_app("menu")
    
    def make_logo(self):
        self.logger.info("Button")
        icons = Icons()
        job = self.tasker.add_job(make_logo, (icons.icons["fontawesome"]), ttl=10)
        self.job_id = job.get_id()
        print(self.job_id)
        self.container.add_child(self.spinner)