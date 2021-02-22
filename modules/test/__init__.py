import pygame as pg
from pycube.components import *
from pycube.core import Application

class App(Application):
    def build(self):
        icon_info = {'name':'fontawesome', 'icon':'apple', 'size':50, 'color':TCOLOR, 'scale': 'auto', 'onClick': self.changeColor, 'onClickData':BGCOLOR}
        icon_info2 = {'name':'fontawesome', 'icon':'apple', 'size':50, 'color':TCOLOR, 'scale': 'auto', 'onClick': self.changeColor, 'onClickData': BLUE}
        icon_info3 = {'name':'fontawesome', 'icon':'wifi', 'size':50, 'color':TCOLOR, 'scale': 'auto', 'onClick': self.test}
        btn_info = {'color': TCOLOR, 'onClick': self.quit, 'width': 40, 'height': 40, 'text':'Quit', 'textColor':WARNING}
        self.name = 'test'
        icon = Icons()
        self.vbox = VScrollView((260,50), width=200, height=200, border=2, borderColor=RED)
        for i in range(10):
            l = Label((10,0), text=f" Hello{i} ", size=30, borderColor=WHITE, onClick=self.selected_text, onClickData=f"Hello{i}")
            self.vbox.add_child(l)
        self.i = IconImage((10,10),icon, **icon_info)
        self.i2 = IconImage((100,10),icon, **icon_info2)
        self.i3 = IconImage((10, 60), icon, **icon_info3)
        c = Container((50,5), width=200, height=200, border=3)
        c.add_child(self.i)
        c.add_child(self.i2)
        c.add_child(self.i3)
        self.b = Button((100, 70), **btn_info)
        c.add_child(self.b)
        self.container.add_child(c)
        self.container.add_child(self.vbox)

    def selected_text(self, *text):
        print("".join(text))

    def changeColor(self, *color):
        print("Testing")
        print(color)
        self.container.backgroundColor = color

    def test(self):
        print('Test')
        icon_info = {'name':'fontawesome', 'icon':'wifi', 'size':100, 'color':TCOLOR, 'scale': 'auto'}
        icons = Icons()
        icon =IconImage((0,0), icons, **icon_info)
        pg.image.save(icon.surface, "logo.png")
        ##self.controller.switch_app('test2')

    def controls(self):
        if pg.K_a in self.events:
            self.i.click()
        elif pg.K_s in self.events:
            self.i2.click()
        elif pg.K_d in self.events:
            self.i3.click()
        elif (pg.K_k in self.events) and (pg.K_l in self.events):
            self.b.click()
        elif pg.K_RIGHT in self.events:
            self.container.selected_child().next_child()
        elif pg.K_LEFT in self.events:
            self.container.selected_child().prev_child()
        elif pg.K_RETURN in self.events:
            #self.container.selected_child().selected_child().click()
            self.vbox.selected_child().click()
        if(pg.K_UP in self.events):
            self.vbox.prev()
        elif(pg.K_DOWN in self.events):
            self.vbox.next()
        for child in self.vbox.childComponents:
            child.border = 0
        self.vbox.selected_child().border=3

    def quit(self):
        self.controller.quit()

    def onStart(self):
        self.logger.info(self.events)