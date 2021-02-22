import netifaces
import psutil
from psutil._common import bytes2human
from pycube.components import *
from pycube.core import Application

class App(Application):
    def onStart(self):
        container = HBox((10,10), width=SCREEN_WIDTH, height=SCREEN_HEIGHT, border=2, borderColor=WHITE)
        self.ipaddressContainer = VBox((0,0), width=215, height=220, border=2, borderColor=WHITE)
        self.memContainer = VBox((0,0), width=215, height=220, border=2, borderColor=WHITE)
        self.update_ipaddress()
        self.update_cpu_ram()
        container.add_child(self.ipaddressContainer)
        container.add_child(Line((0,0), width=2, height=220, horizontal=False, color=WHITE))
        container.add_child(self.memContainer)
        self.container.add_child(container)
    
    def update_cpu_ram(self):
        self.memContainer.clear_children()
        cpu_counts = psutil.cpu_count(logical=False)
        cpu_threads = psutil.cpu_count() / psutil.cpu_count(logical=False)
        cpu_percent = Label((0,0), text=f"CPU: {psutil.cpu_percent()}%")
        cpu_count = Label((0,0), text=f"CPU Count: {cpu_counts}")
        cpu_thread  = Label((0,0), text=f"CPU Thread: {cpu_threads}")
        
        ram = psutil.virtual_memory()
        swap = psutil.swap_memory()
        ram_avail = Label((0,0), text=f"Ram Avail: {bytes2human(ram.available)}")
        ram_total = Label((0,0), text=f"Ram Total: {bytes2human(ram.total)}")
        ram_percent = Label((0,0), text=f"RAM: {bytes2human(ram.percent)}%")

        swap_free = Label((0,0), text=f"Swap Free: {bytes2human(swap.free)}")
        swap_total = Label((0,0), text=f"Swap Total: {bytes2human(swap.total)}")
        swap_percent = Label((0,0), text=f"Swap: {bytes2human(swap.percent)}%")

        self.memContainer.add_child(cpu_percent)
        self.memContainer.add_child(cpu_count)
        self.memContainer.add_child(cpu_thread)

        self.memContainer.add_child(Line((0,0), width=200, height=2, color=WHITE))
        self.memContainer.add_child(ram_percent)
        self.memContainer.add_child(ram_total)
        self.memContainer.add_child(ram_avail)
        
        self.memContainer.add_child(Line((0,0), width=200, height=2, color=WHITE))
        self.memContainer.add_child(swap_percent)
        self.memContainer.add_child(swap_total)
        self.memContainer.add_child(swap_free)

    def update_ipaddress(self):
        interfaces = netifaces.interfaces()
        self.ipaddressContainer.clear_children()
        for interface in interfaces:
            ip = netifaces.ifaddresses(interface)
            if 2 in ip:
                hbox = HBox((0,0), width=190, height=20)
                hbox.add_child(Label((0,0), text=interface))
                hbox.add_child(Label((0,0), text=ip[2][0]["addr"]))
                self.ipaddressContainer.add_child(hbox)