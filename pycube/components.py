import os
from typing import List, Dict, Any, Tuple
import pygame as pg
from copy import deepcopy
from datetime import datetime
from pycube.eventHandler import *
from .utils import *
from .settings import *
from .icon_font import *


class Font(object):
    def __init__(self, name: str, minSize: int = 10, maxSize: int = 30, ft_support: bool = False):
        self.path = get_font(font_dir, name)
        current_size = minSize
        self.sizes = {}
        self.ft_support = ft_support
        self.ft_sizes = {}
        while current_size <= maxSize:
            if self.ft_support:
                try:
                    self.ft_sizes[current_size] = pg.freetype.Font(path, current_size)
                except:
                    self.ft_support = False
            elif os.path.isfile(self.path):
                self.sizes[current_size] = pg.font.Font(self.path, current_size)
            else:
                self.sizes[current_size] = pg.font.SysFont(self.path, current_size)
            current_size += 1

    def get(self, size: int = 14, ft: bool = False):
        if ft and self.ft_support:
            if size not in self.ft_sizes:
                try:
                    self.ft_sizes[size] = pg.freetype.Font(self.path, size)
                except:
                    return None
            return self.ft_sizes[size]
        else:
            if size not in self.sizes:
                if os.path.isfile(self.path):
                    self.sizes[size] = pg.font.Font(self.path, size)
                else:
                    return None
            return self.sizes[size]

    def draw_text(self, largeSurface: pg.Surface, text: str, x: int, y: int, size: int = 14, color: Tuple = TCOLOR):
        font = self.get(size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        largeSurface.blit(text_surface, text_rect)

fonts = {"lobster":Font("lobster"), "roboto": Font("roboto-regular"), "transformer": Font("transformer"), "batman": Font("batman_forever")}

class ColorPalette(object):
    def __init__(self):
        self.palette = {
                        'background': BLACK,
                        'item': WHITE,
                        'accent': ACCENT,
                        'warning': WARNING,
                        'error': ERROR
                        }

    def getPalette(self):
        return self.palette

    def getColor(self, item: str):
        return self.palette[item]

    def setScheme(self):
        pass

    def add(self, name: str, color: Tuple):
        self.palette[name] = color

class Icons(object):
    def __init__(self):
        self.icons = {}
        self.add_icon(FONTAWESOME)

    def add_icon(self, icon_info: Dict):
        icon = IconFont(css_file=icon_info['css'], ttf_file=icon_info['ttf'])
        self.icons[icon_info['name']] = icon

    def get_icons(self):
        return self.icons

    def get_icon(self, name: str, icon: str, size: int = 20, color: str = "black",scale: str= "auto"):
        if self.icons:
            return self.icons[name].pygame_image(icon, size, color, scale)
        else:
            print("[INFO] You need to load the Icon font first")

class Component(object):
    def __init__(self, position: Tuple,**data):
        self.position = list(position)[:]
        self.width = -1
        self.height = -1
        self.eventBindings = {}
        self.eventData = {}
        self.surface = None
        self.border = 0
        self.borderColor = (0,0,0)
        self.hide = data.get('hide',False)
        if 'surface' in data:
            self.surface = data['surface']
            if 'width' in data or 'height' in data:
                if 'width' in data:
                    self.width = data['width']
                    self.height = self.surface.get_height()
                if 'height' in data:
                    self.height = data['height']
                    if self.width == -1:
                        self.width = self.surface.get_width()
                self.surface = pygame.transform.scale(self.surface, (self.width, self.height))
            else:
                self.width = self.surface.get_width()
                self.height = self.surface.get_height()
        else:
            self.width = data['width']
            self.height = data['height']
            self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()

        if 'onClick' in data:
            self.eventBindings['onClick'] = data['onClick']
        if 'onClickData' in data:
            self.eventData['onClick'] = data['onClickData']
        if 'border' in data:
            self.border = int(data['border'])
            if 'borderColor' in data:
                self.borderColor = data['borderColor']
        self.parent = None
        self.old_surface = self.surface.copy()

    def on_click(self):
        if 'onClick' in self.eventBindings:
            if 'onClick' in self.eventData:
                self.eventBindings['onClick'](*self.eventData['onClick'])
            else:
                self.eventBindings['onClick']()

    def click(self):
        self.on_click()

    def set_on_click_data(self,data=None):
        self.eventData['onClick'] = data

    def draw(self, largeSurface: pg.Surface):
        if self.rect.x != self.position[0]:
            self.rect.x = self.position[0]
        if self.rect.y != self.position[1]:
            self.rect.y = self.position[1]
        if self.rect.w != self.width:
            self.rect.w = self.width
        if self.rect.h != self.height:
            self.rect.h = self.height

        if self.border > 0:
            pygame.draw.rect(self.surface, self.borderColor,[0,0,self.width,self.height], self.border)
        largeSurface.blit(self.surface, self.rect)

    def update(self):
        pass

    def check_click(self, mouseEvent, offsetX: int = 0, offsetY: int = 0):
        adjusted = [mouseEvent.pos[0] - offsetX, mouseEvent.pos[1] - offsetY]
        if adjusted[0] >= self.position[0] and adjusted[0] <= self.position[0] + self.width:
            if adjusted[1] >= self.position[1] and adjusted[1] <= self.position[1] + self.height:
                return True
        return False

    def set_position(self, pos: Tuple):
        self.position = list(pos)[:]

class Image(Component):
    def __init__(self, position: Tuple, **data):
        super(Image, self).__init__(position, **data)
        self.img = data.get("image")
        if self.img:
            self.set_pygame_img(self.img)
        path = data.get("path")
        if path:
            self.get_image(path)

    def get_image(self, img: str):
        self.img = pg.image.load(img).convert_alpha()
        self.surface = pg.transform.scale(self.img, (self.width, self.height))
    
    def set_pygame_img(self, img: pg.Surface):
        self.surface = img

class IconImage(Component):
    def __init__(self, position: Tuple, icons: Icons, **data):
        self.surface = icons.get_icon(data['name'], data['icon'], data['size'], data['color'], data['scale'])
        data['width'] = data['size']
        data['height'] = data['size']
        data['surface'] = self.surface
        self.originalSurface = self.surface.copy()
        super(IconImage, self).__init__(position, **data)
        self.need_update = True
        self.pos = self.position
        self.rect = self.get_rect()

    def update(self):
        if self.need_update:
            self.surface = pg.transform.scale(self.originalSurface, (self.width, self.height))
            self.rect = self.get_rect()
            self.rect.x = self.position[0]
            self.rect.y = self.position[1]
            self.need_update = False

    def set_icon(self, surface: pg.Surface):
        self.originalSurface = surface.copy()
        self.need_update = True
        self.update()

    def get_rect(self):
        return self.surface.get_rect()

    def rotate(self, rotation: int):
        newSurface = pg.transform.rotate(self.originalSurface, -rotation)
        rect = self.surface.get_rect()
        self.position = (self.pos[0] - (self.width / 2), self.pos[1] - (self.height / 2)) #(rect.x, rect.y)
        #self.surface = pg.transform.scale(newSurface, (self.width, self.height))
        self.surface = newSurface

    def vflip(self):
        self.surface = pg.transform.flip(self.originalSurface, True, False)

    def hflip(self):
        self.surface = pg.transform.flip(self.originalSurface, False, True)

class Container(Component):

    def __init__(self, position: Tuple, **data):
        super(Container, self).__init__(position, **data)
        self.transparent = False
        self.backgroundColor = BGCOLOR
        self.childComponents = []
        self.selected = 0
        self.SkipChildCheck = False
        if 'transparent' in data:
            self.transparent = data['transparent']
        if 'color' in data:
            self.backgroundColor = data['color']
        if 'children' in data:
            self.childComponents = data['children']
        if 'backgroundColor' in data:
            self.backgroundColor = data['backgroundColor']
        if 'description' in data:
            self.description = data['description']
        else:
            self.description = ''

    def add_child(self, component: Component):
        component.parent = self
        self.childComponents.append(component)

    def selected_child(self):
        if len(self.childComponents) > 0:
            return self.childComponents[self.selected]
        return None

    def next_child(self):
        if (self.selected < len(self.childComponents) - 1):
            self.selected += 1

    def prev_child(self):
        if (self.selected > 0):
            self.selected -= 1

    def remove_child(self, component: Component):
        self.childComponents.remove(component)

    def clear_children(self):
        self.childComponents.clear()

    def get_clicked_child(self, mouseEvent, offsetX: int = 0, offsetY: int = 0):
        currChild = len(self.childComponents)
        while currChild > 0:
            currChild -= 1
            child = self.childComponents[currChild]
            if "SkipChildCheck" in child.__dict__:
                if child.SkipChildCheck:
                    if child.check_click(mouseEvent, offsetX + self.position[0], offsetY + self.position[1]):
                        return child
                    else:
                        continue
                else:
                    subcheck = child.get_clicked_child(mouseEvent, offsetX + self.position[0], offsetY + self.position[1])
                    if subcheck == None:
                        continue
                    return subcheck
            else:
                if child.check_click(mouseEvent, offsetX + self.position[0], offsetY + self.position[1]):
                    return child
        if self.check_click(mouseEvent, offsetX, offsetY):
            return self
        return None

    def get_child_at(self, position: Tuple):
        for child in self.childComponents:
            if child.position == list(position):
                return child
        return None

    def get_child(self, index: int):
        if (index >= 0 and index < len(self.childComponents)):
            return self.childComponents[index]
    
    def draw(self, largeSurface: pg.Surface):
        if not self.transparent:
            self.surface.fill((self.backgroundColor))
        else:
            self.surface.fill((0,0,0,0))
        for child in self.childComponents:
            if not child.hide:
                child.draw(self.surface)
        super(Container, self).draw(largeSurface)

    def update(self, children: bool = True):
        super(Container, self).update()
        if children:
            for child in self.childComponents:
                child.update()

class HexContainer(Container):

    def __init__(self, position: Tuple, size: int, color=(255,255,255), backgroundColor=(100,100,200), orientation=1, **data):
        self.hexPoints = hexagon(size,size,size,orientation)
        self.diameter = size * 2
        self.width = self.diameter
        self.height= self.diameter
        self.position = list(position)[:]
        data['width'] = self.width
        data['height'] = self.height
        self.surface = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)
        super(HexContainer, self).__init__(position, **data)
        self.color = color
        self.backgroundColor = backgroundColor
        self.holdBackgroundColor = backgroundColor
        self.surface = self.hexSurface()
        self.is_activated = False

    def getSurface(self):
        self.surface = pg.Surface((self.diameter, self.diameter), pg.SRCALPHA)
    
    def hexSurface(self):
        pygame.draw.polygon(self.surface,self.backgroundColor,self.hexPoints)
        pygame.draw.polygon(self.surface, self.color, self.hexPoints, self.border)
        return self.surface

    def set_content(self, child):
        child.position = get_centered_coordinates(child, self)
        self.add_child(child)

    def draw(self, largeSurface):
        self.update()
        largeSurface.blit(self.surface, self.position)
    
    def update(self, children: bool = True):
        self.surface = self.hexSurface()
        if children:
            for child in self.childComponents:
                child.draw(self.surface)
    
    def toggle(self):
        if self.is_activated:
            self.is_activated = False
            self.backgroundColor = self.holdBackgroundColor
        else:
            self.is_activated = True
            self.backgroundColor = (0,0,0,0)  
    
class CircleContainer(Container):
    def __init__(self, position, **data):
        data["width"] = int(data.get("radius",50)) * 2 + 11
        data["height"] = int(data.get("radius",50)) * 2 + 11
        super(CircleContainer, self).__init__(position, **data)
        #self.transparent = data.get("transparent", True)
        self.SkipChildCheck = data.get("SkipChildCheck", True)
        self.circleColor = data.get("circleColor",(TCOLOR))
        self.radius = data.get("radius",50)
        self.circle = Circle((5,5), radius=self.radius, color=self.circleColor, thickness=data.get("thickness", 1))
        self.outter = Circle((0,0), radius=self.radius + 5)
        self.add_child(self.circle)
        self.add_child(self.outter)
        self.is_activated = True
        self.outter.hide = self.is_activated
    
    def toggle(self):
        if self.is_activated:
            self.is_activated = False
        else:
            self.is_activated = True
        self.outter.hide = self.is_activated

    def set_content(self, child):
        child.position = get_centered_coordinates(child, self)
        self.add_child(child)

    def changeColor(self, color):
        self.circle.update_circle(color=color)
    
    def changeRadius(self, radius):
        self.width = radius * 2
        self.height = self.width
        self.circle.update_circle(radius=radius)

class Button(Container):
    def __init__(self, position, bgColor=(20,20,20), **data):
        self.text = Label((0,0), text=data.get('text',''), size=data.get('size',14), color=data.get('textColor',TCOLOR))
        self.SkipChildCheck = True
        self.padding = data.get("padding", 10)
        if "width" not in data:
            data["width"] = self.text.width + self.padding
        if "height" not in data:
            data["height"] = self.text.height + self.padding
        super(Button, self).__init__(position, **data)
        self.text.position = get_centered_coordinates(self.text, self)
        self.add_child(self.text)
        self.backgroundColor = data.get("backgroundColor", (20,20,20))

    def set_text(self, text):
        self.text.set_text(text)

class HBox(Container):
    def __init__(self, position, **data):
        data["width"] = data.get("width", WIDTH - 10)
        data["height"] = data.get("height", HEIGHT - 70)
        super(HBox, self).__init__(position, **data)
        self.container = Container((0,0),width = self.width , height = self.height)
        self.spacing = data.get("spacing", 5)

    def add_child(self, component):
        component.parent = self
        component.position[1] = get_centered_coordinates(component, self)[1]
        if (len(self.childComponents) > 0):
            last_child = self.childComponents[-1]
            component.position[0] = last_child.position[0] + last_child.width + self.spacing
        else:
            component.position[0] = 5
        self.childComponents.append(component)
    
class HScrollView(HBox):
    #def __init__(self, position, **data):
        #super(HScrollView, self).__init__(position, **data)
    
    def next(self):
        self.next_child()
        if(self.selected_child().position[0] > self.width):
            for child in self.childComponents:
                child.position[0] -= (self.selected_child().width + self.spacing)

    def prev(self):
        self.prev_child()
        if(self.selected_child().position[0] < 0):
            for child in self.childComponents:
                child.position[0] += (self.selected_child().width + self.spacing)

class VBox(Container):
    def __init__(self, position: Tuple = (0,0), **data):
        super(VBox, self).__init__(position, **data)
        self.container = Container((0,0),width = data.get("width", WIDTH - 10), height= data.get("height", HEIGHT - 30))
        self.spacing = data.get("spacing", 5)

    def add_child(self, component):
        component.parent = self
        #component.position[1] = get_centered_coordinates(component, self)[1]
        if (len(self.childComponents) > 0):
            last_child = self.childComponents[-1]
            component.position[1] = last_child.position[1] + last_child.height + self.spacing
            component.position[0] = 5
        else:
            component.position[1] = 5
            component.position[0] = 5
        self.childComponents.append(component)

class VScrollView(VBox):
    def next(self):
        if not self.hide:
            self.next_child()
            if(self.selected_child().position[1] + self.selected_child().height - 10 > (self.height - self.spacing)):
                for child in self.childComponents:
                    child.position[1] -= self.selected_child().height + self.spacing

    def prev(self):
        if not self.hide:
            self.prev_child()
            if(self.selected_child().position[1] < 0):
                for child in self.childComponents:
                    child.position[1] += (self.selected_child().height + self.spacing)

class FileHolder(Container):
    def __init__(self, position=(10,0), **data):
        super(FileHolder, self).__init__(position, **data)
        self.content = data.get("content","")
        self.SkipChildCheck = True
        label = Label((0,0), text=self.content.split("/")[-1])
        self.hbox = HBox((0,0), width=self.width, height=self.height)
        if(os.path.isfile(self.content)):
            img = Image((0,0), width=16,height =16, image=file_img)
            self.hbox.add_child(img)
        elif (os.path.isdir(self.content)):
            img = Image((0,0), width=16,height =16, image=folder_img)
            self.hbox.add_child(img)
        self.hbox.add_child(label)
        self.add_child(self.hbox)

    def set_border(self, border: int = 0):
        self.hbox.border = border

class FileDialog(Container):
    def __init__(self, position: Tuple = (0,0),**data):
        data["width"] = WIDTH - 20
        data["height"] = HEIGHT - 80
        super(FileDialog, self).__init__(position, **data)
        self.rootPath = os.path.join("/home", os.listdir("/home")[0])
        self.fileContainer = VScrollView((0,0), width = WIDTH - 20, height = HEIGHT - 80, border=2)
        self.add_child(self.fileContainer)
        self.current_child = 0
        self.update_container()

    def update_container(self):
        self.fileContainer.clear_children()
        self.fileContainer.selected = 0
        for i in os.listdir(self.rootPath):
            if i.startswith("."):
                continue
            path = os.path.join(self.rootPath, i)
            self.fileContainer.add_child(FileHolder(content = path, width = self.fileContainer.width - 20, height= 20, onClick=self.update_path, onClickData=path))
        #self.fileContainer.get_child(self.current_child).selected(True)
        self.update_children()

    def  update_path(self, *path):
        path = "".join(path)
        if(os.path.isdir(path)):
            self.rootPath = path
            self.update_container()

    def go_back(self) -> str:
        if not self.hide:
            path = self.rootPath.split("/")
            path.pop()
            path = "/".join(path)
            if path != "":
                self.rootPath = path
                self.update_container()
                return self.rootPath
        return None
    
    def enter(self) -> str:
        if not self.hide:
            if len(self.fileContainer.childComponents) > 0:
                print(len(self.fileContainer.childComponents))
                self.fileContainer.selected_child().click()
                if self.fileContainer.selected_child() and os.path.isfile(self.fileContainer.selected_child().content):
                    print("Testing")
                    self.hide = True
                    return self.fileContainer.selected_child().content
                return self.rootPath
        return None

    def go_down(self):
        if not self.hide:
            self.fileContainer.next()
            self.update_children()
    
    def go_up(self):
        if not self.hide:
            self.fileContainer.prev()
            self.update_children()
    
    def update_children(self):
        if self.fileContainer.childComponents:
            for child in self.fileContainer.childComponents:
                child.border = 0
            self.fileContainer.selected_child().border = 2

class PagedContainer(Container):
    def __init__(self, position: Tuple =(0,0), **data):
        pass

class ContainerEvent(Container):

    def __init__(self, position: Tuple = (0,0), **data):
        super(ContainerEvent, self).__init__(position, **data)
        self.triggers = data.get("triggers", [])
    
    def run_triggers(self, events: List[str]):
        for trigger in self.triggers:
            if trigger.event.type in events:
                trigger.fire()

class Screen(Container):
    """
    This is a screen components that can hold on once child at a time.
    The only type of child it can hold is ContainerEvent
    """

    def add_child(self, component: ContainerEvent):
        self.clear_children()
        return super().add_child(component)
    
    def events(self, events):
        self.childComponents[0].run_triggers(events)


class KeyboardButton(Container):
    def __init__(self, position, symbol, altSymbol, **data):
        if "border" not in data:
            data["border"] = 1
            data["borderColor"] = (BLACK)
        super(KeyboardButton, self).__init__(position, **data)
        self.SkipChildCheck = True
        self.primaryText = Label((0,0), text = symbol, color = BLACK, size = 20)
        self.secondaryText = Label((self.width -8, 0), text = altSymbol, color = BLACK, size = 10) 
        self.primaryText.position = (get_centered_coordinates(self.primaryText, self)[0] - 6, self.height - self.primaryText.height - 1) 
        self.add_child(self.primaryText)
        self.add_child(self.secondaryText)     

    def swapText(self):
        primaryText = self.primaryText.text
        secondaryText = self.secondaryText.text 
        self.primaryText.set_text(secondaryText)
        self.secondaryText.set_text(primaryText)
        self.set_on_click_data(secondaryText)

class TextEntryField(Container):
    def __init__(self, position: Tuple, app, initialText: str="", **data):
        data["onClick"] = self.parseClick
        if "border" not in data:
            data["border"] = 1
            data["borderColor"] = BLACK
        if "textColor" not in data:
            data["textColor"] = BLACK
        if "blink" in data:
            self.blickInterval = data["blink"]
        else:
            self.blickInterval = 500

        self.firstClick = True

        self.doBlink = False
        self.blinkOn = False
        self.lastBlick = datetime.now()
        self.indicatorPosition = len(initialText)
        self.indicatorPxPosition = 0
        super(TextEntryField, self).__init__(position, **data)
        self.SkipChildCheck = True
        self.textComponent = Label((2,0), text=initialText, color=data["textColor"], size=14)
        self.textComponent.position[1] = get_centered_coordinates(self.textComponent, self)[1]
        self.add_child(self.textComponent)
        self.app = app

    def parseClick(self):
        if self.firstClick:
            self.firstClick = False
            self.textComponent.set_text("")
        
        if self.app.keyboard == None:
            self.app.keyboard = Keyboard(self)
        
        if self.app.keyboard.textEntryField != self:
            self.app.keyboard.textEntryField = self
        else:
            self.doBlink = True
            mousePos = list(pg.mouse.get_pos())
            currFont = Font("lobster").get()
            currTextString = ""
            pos = 0
            textWidth = 0
            rendered = None
            while pos < len(self.textComponent.text):
                currTextString = self.textComponent.text[:pos]
                rendered = currFont.render(currTextString, 1, (0,0,0))
                textWidth = rendered.get_width()
                pos += 1
                if self.position[0] - 4 + textWidth <= mousePos[0] <= self.position[0] + 4 + textWidth:
                    break
            
            if mousePos[0] > textWidth:
                self.indicatorPosition = len(self.textComponent.text)
                self.doBlink = False
            else:
                self.indicatorPxPosition = textWidth
                self.indicatorPosition = pos
                self.doBlink = True

        self.app.keyboard.active = True

    def append_char(self, char):
        self.doBlink = False 
        self.textComponent.set_text(self.textComponent.text[:self.indicatorPosition] + char + self.textComponent.text[self.indicatorPosition:])
        self.indicatorPosition += 1
    
    def backspace(self):
        if self.indicatorPosition >= 1:
            self.indicatorPosition -= 1
            self.textComponent.set_text(self.textComponent.text[:self.indicatorPosition] + self.textComponent.text[self.indicatorPosition+1:])
        
    def delete(self):
        if self.indicatorPosition < len(self.textComponent.text):
            self.textComponent.set_text(self.textComponent.text[:self.indicatorPosition] + self.textComponent.text[self.indicatorPosition+1:])
    
    def get_text(self):
        return self.textComponent.text 

    def draw(self, largeSurface):
        if not self.transparent:
            self.surface.fill(self.backgroundColor)
        else:
            self.surface.fill((0,0,0,0))
        
        for child in self.childComponents:
            child.draw(self.surface)
        
        if self.doBlink:
            if ((datetime.now() - self.lastBlick).microseconds / 1000) >= self.blickInterval:
                self.lastBlick = datetime.now()
                self.blinkOn = not self.blinkOn
            if self.blinkOn:
                pg.draw.rect(self.surface, self.textComponent.color, [2+self.indicatorPxPosition, 2, 2, self.height-4])
        
        super(Container, self).draw(largeSurface)

class ButtonRow(Container):
    def __init__(self, position, **data):
        self.padding = 2
        if "padding" in data:
            self.padding = data["padding"]
        self.margin = 2
        if "margin" in data:
            self.margin = data["margin"]
        super(ButtonRow, self).__init__(position, **data)
    
    def get_last_component(self):
        if len(self.childComponents) > 0:
            return self.childComponents[-1]
        return None
    
    def add_child(self, component: Component):
        component.height = self.height - (2 * self.padding)
        last = self.get_last_component()
        if last:
            component.set_position((last.position[0] + last.width++self.margin, self.padding))
        else:
            component.set_position((self.padding, self.padding))
        super(ButtonRow, self).add_child(component)

    def remove_child(self, component: Component):
        super(ButtonRow, self).remove_child(component)
        children = self.childComponents[:]
        self.clear_children()
        for child in children:
            self.add_child(child)
    
class Keyboard(object):
    def __init__(self, textEntryField: TextEntryField = None, onEnter="return"):
        self.onEnter = onEnter
        self.shiftUp = False 
        self.active = False
        self.textEntryField = textEntryField
        self.baseContainer = None
        baseContainerHeight = 100
        self.originalTextEntryFieldPosition = self.textEntryField.position[:]
        self.keyboardContainer = Container((0, HEIGHT - 130), width = WIDTH, height=100)
        self.keyWidth = self.keyboardContainer.width / 10
        self.keyHeight = self.keyboardContainer.height / 4
        self.selected = 0
        self.row = 0
        self.lastTime = 0
        EventClose = Event("1", self.deactivate)
        Event1 = Event("Up", self.rowHandler)
        Event2 = Event('Down', self.rowHandler)
        Event3 = Event('3', self.deactivate)
        Event4 = Event('Right', self.columnHandler)
        Event5 = Event('Left', self.columnHandler)
        Event6 = Event('6', self.click)
        Event7 = Event('7', self.alternate)
        Event8 = Event('8', self.backspace)
        dispatch = EventDispatcher()

        self.TriggerClose = Trigger(dispatch, EventClose)
        self.Trigger1 = Trigger(dispatch, Event1)
        self.Trigger2 = Trigger(dispatch, Event2)
        self.Trigger3 = Trigger(dispatch, Event3)
        self.Trigger4 = Trigger(dispatch, Event4)
        self.Trigger5 = Trigger(dispatch, Event5)
        self.Trigger6 = Trigger(dispatch, Event6)
        self.Trigger7 = Trigger(dispatch, Event7)
        self.Trigger8 = Trigger(dispatch, Event8)

        ListenerClose = Listener(dispatch, EventClose)
        Listener1 = Listener(dispatch, Event1)
        Listener2 = Listener(dispatch, Event2)
        Listener3 = Listener(dispatch, Event3)
        Listener4 = Listener(dispatch, Event4)
        Listener5 = Listener(dispatch, Event5)
        Listener6 = Listener(dispatch, Event6)
        Listener7 = Listener(dispatch, Event7)
        Listener8 = Listener(dispatch, Event8)

        self.press6 = True
        self.press8 = True
        self.press7 = True

        self.shiftSym = "sh"
        self.enterSym = "->"
        self.bckspcSym = "<-"
        self.deleteSym = "del"
        self.specialKeys = [self.shiftSym, self.enterSym, self.bckspcSym, self.deleteSym]

        self.keys1 = [['q','w','e','r','t','y','u','i','o','p'],
                        ['a','s','d','f','g','h','j','k','l',self.enterSym],
                        [self.shiftSym, 'z','x','c','v','b','n','m',',','.'],
                        ['!','?',' ','','','','','-','"',self.bckspcSym]]
        self.keys2 = [['1','2','3','4','5','6','7','8','9','0'],
                        ['@','#','$','%','^','&','*','(',')','_'],
                        ['=','+','\\','/','<','>','|','[',']',':'],
                        [';','{','}','','','','','-','\"',self.deleteSym]]
        row = 0

        for symrow in self.keys1:
            sym = 0
            for symbol in symrow:
                button = None
                if symbol == "":
                    sym += 1
                    continue
                if symbol == " ":
                    button = KeyboardButton((sym * self.keyWidth, row * self.keyHeight), "", self.keys2[row][sym],
                                            onClick=self.insertChar, onClickData=(self.keys1[row][sym],),
                                            width=self.keyWidth*5, height=self.keyHeight)
                else:
                    if symbol in self.specialKeys:
                        button = KeyboardButton((sym * self.keyWidth, row * self.keyHeight), self.keys1[row][sym],
                                                self.keys2[row][sym], onClick=self.insertChar, onClickData=(self.keys1[row][sym],),
                                                width=self.keyWidth, height=self.keyHeight)
                    else:
                        button = KeyboardButton((sym  * self.keyWidth, row * self.keyHeight), self.keys1[row][sym], self.keys2[row][sym],
                                                onClick=self.insertChar, onClickData=(self.keys1[row][sym],), width=self.keyWidth, height=self.keyHeight)
                self.keyboardContainer.add_child(button)
                sym += 1
            row += 1
        
        self.baseContainer = self.keyboardContainer
        self.keyboardContainer.childComponents[0].backgroundColor = (200,200, 200, 100)

    def rowHandler(self, event: Event = None):
        if event.type == "Up":
            if self.row == 0:
                return
            else:
                self.row -= 1
                if (self.selected >= 33 and self.selected <= 35):
                    self.selected -= 6
                else:
                    self.selected -= 10
        
        elif event.type == "Down":
            if self.row == 3:
                return
            else:
                self.row += 1
                if (self.selected >= 26 and self.selected <= 29):
                    self.selected += 6
                elif self.selected == 23:
                    self.selected += 9
                elif self.selected == 24:
                    self.selected += 8
                elif self.selected == 25:
                    self.selected += 7
                else:
                    self.selected += 10
        
        print(f"Keyboard: [{self.selected}]")
        self.update_children((200,200,200,100))
    
    def columnHandler(self, event: Event = None):
        if event.type == "Right" and self.selected < 35:
            self.selected += 1
        
        if event.type == "Left" and self.selected > 0:
            self.selected -= 1

        if (self.selected >= 0 and self.selected <= 9):
            self.row = 0
        elif (self.selected >= 10 and self.selected <= 19):
            self.row = 1
        elif (self.selected >= 20 and self.selected <= 29):
            self.row = 2
        elif (self.selected >= 30 and self.selected < 35):
            self.row = 3
        
        self.update_children((200, 200, 200, 100))
    
    def alternate(self, event: Event = None):
        for button in self.baseContainer.childComponents:
            button.swapText()

    def update_children(self, color: Tuple):
        for index, child in enumerate(self.keyboardContainer.childComponents):
            if index == self.selected:
                child.backgroundColor = color
            else:
                child.backgroundColor = (0,0,0, 0)
    
    def backspace(self, event: Event = None):
        self.textEntryField.backspace()
    
    def get_events(self, gamepad):
        bsp, analog = gamepad
        if "1" in bsp:
            self.TriggerClose.fire()
            return None
        
        if "Up" in bsp:
            self.Trigger1.fire()
        if "Down" in bsp:
            self.Trigger2.fire()
        if "3" in bsp:
            self.Trigger3.fire()
        if "Right" in bsp:
            self.Trigger4.fire()
        if "Left" in bsp:
            self.Trigger5.fire()
        if "6" in bsp:
            if not self.press6:
                self.Trigger6.fire()
                self.press6 = True
        else:
            self.press6 = False
        
        if "7" in bsp:
            if not self.press7:
                self.Trigger7.fire()
                self.press7 = True
        else:
            self.press7 = False

        if "8" in bsp:
            if not self.press8:
                self.press8 = True 
                self.Trigger8.fire()
        else:
            self.press8 = False
    
    def click(self, event: Event = None):
        self.keyboardContainer.childComponents[self.selected].click()
    
    def set_on_enter(self, value="return"):
        self.onEnter = value

    def deactivate(self, event: Event = None):
        self.active = False
        self.textEntryField = None
    
    def setTextEntryField(self, field: TextEntryField):
        self.textEntryField = field 
        self.active = True
    
    def get_entered_text(self):
        return self.textEntryField.get_text()
    
    def insertChar(self, char):
        if char == self.shiftSym or char == self.shiftSym.upper():
            self.shiftUp = not self.shiftUp
            for index, button in enumerate(self.baseContainer.childComponents):
                if self.shiftUp:
                    button.primaryText.set_text(button.primaryText.text.upper())
                else:
                    button.primaryText.set_text(button.primaryText.text.lower())
            return

        if char == self.enterSym:
            if self.onEnter == "newline":
                pass
            else:
                self.deactivate()
            return

        if char == self.bckspcSym:
            self.textEntryField.backspace()
            return 

        if char == self.deleteSym:
            self.textEntryField.delete()
            return 
        
        if self.shiftUp:
            self.textEntryField.append_char(char.upper())
        else:
            self.textEntryField.append_char(char)

    
    def draw(self, largeSurface: pg.Surface):
        self.keyboardContainer.draw(largeSurface)

    def get_clicked_child(self, event):
        child = self.keyboardContainer.get_clicked_child(event)
        if child:
            child.on_click()
        else:
            self.deactivate()

    def event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.Trigger1.fire()
            elif event.key == pg.K_DOWN:
                self.Trigger2.fire()
            elif event.key == pg.K_LEFT:
                self.Trigger5.fire()
            elif event.key == pg.K_RIGHT:
                self.Trigger4.fire()
            elif event.key == pg.K_RETURN:
                self.Trigger6.fire()
            elif event.key == pg.K_BACKSPACE:
                self.Trigger8.fire()

########### Component ########### 
class Label(Component):
    def __init__(self, position, **data):
        self.text = data.get('text','')
        self.size = data.get('size', 14)
        self.color = data.get('color',TCOLOR)
        self.font = data.get('font',fonts["roboto"])
        self.oldText = ''
        self.padding = data.get("padding", 0)
        self.update()
        data['surface'] = self.get_text()
        super(Label, self).__init__(position, **data)
        self.update()


    def get_text(self):
        return self.font.get(self.size).render(str(self.text), 1, self.color)

    def update(self):
        if self.oldText != self.text:
            self.surface = self.get_text()
            self.width = self.surface.get_width()
            self.height = self.surface.get_height()

    def set_text(self, text):
        self.oldText = self.text
        self.text = str(text)
        self.update()

class MultiLineText(Component):

    def __init__(self, position: Tuple = (0,0), width: int = 50, height : int = 50, **data):
        self.width = width
        self.height = height
        self.text = data.get('text','')
        self.size = data.get('size', 14)
        self.color = data.get('color',TCOLOR)
        self.font = data.get('font',fonts["roboto"])
        self.oldText = ''
        self.padding = data.get('padding',0)
        self.backgroundColor = data.get("backgroundColor", (0,0,0,0))
        data['surface'] = self.get_text()
        super(MultiLineText, self).__init__(position, **data)

    def get_text(self):
        surface = pg.Surface((self.width, self.height), pygame.SRCALPHA)
        surface.fill(self.backgroundColor)
        words = [word.split(" ") for word in self.text.splitlines()]
        space = self.font.get(self.size).size(" ")[0]
        x,y = self.padding, self.padding
        for line in words:
            for word in line:
                word_surface = self.font.get(self.size).render(str(word), 1, self.color)
                word_width, word_height = word_surface.get_size()
                if x + self.padding + word_width >= self.width:
                    x = self.padding
                    y += word_height
                surface.blit(word_surface, (x,y))
                x += word_width + space 
            x = self.padding
            y += word_height
        return surface

    def update(self):
        if self.oldText != self.text:
            self.surface = self.get_text()
            self.width = self.surface.get_width()
            self.height = self.surface.get_height()

    def set_text(self, text):
        self.oldText = self.text
        self.text = str(text)
        self.update()


class Circle(Component):
    def __init__(self, position, **data):
        self.radius = data.get("radius", 50)
        self.thickness = data.get("thickness", 1)
        self.width = self.radius * 2
        self.height = self.width
        self.color = data.get("color", TCOLOR)
        data["surface"] = self.get_circle()
        super(Circle,self).__init__(position, **data)

    def get_circle(self):
        screen = pg.Surface((self.width, self.height),pg.SRCALPHA)
        pg.draw.circle(screen, self.color, (self.radius,self.radius), self.radius, self.thickness)
        return screen
    
    def update_circle(self, radius=None, color=None, thickness=None):
        self.radius = radius if radius != None else self.radius
        self.width = self.radius * 2
        self.height = self.width
        self.color = color if color != None else self.color
        self.thickness = thickness if thickness != None else self.thickness
        self.surface = pygame.Surface((self.width, self.height),pygame.SRCALPHA)
        pg.draw.circle(self.surface, self.color, (self.radius,self.radius), self.radius, self.thickness)

class Line(Component):
    def __init__(self, position, **data):
        self.width = data.get("width")
        self.height = data.get("height")
        self.color = data.get("color", TCOLOR)
        self.horizontal = data.get("horizontal", True)
        data["surface"] = self.get_line()
        super(Line, self).__init__(position, **data)

    def get_line(self):
        screen = pg.Surface((self.width, self.height), pygame.SRCALPHA)
        if self.horizontal:
            pg.draw.line(screen, self.color, (0,0), (self.width, 0), self.height)
        else:
            pg.draw.line(screen, self.color, (0,0), (0, self.height), self.width)
        return screen

    def update_line(self, width=None, height=None, color = None):
        self.color = color if color != None else self.color
        self.width = width if width != None else self.width
        self.height = height if height != None else self.height
        self.surface = self.get_line()
        
class Slider(Component):
    def __init__(self, position, **data):
        super(Slider, self).__init__(position, **data)
        self.percent = data.get("initialPct", 0)
        self.color = data.get("color", RED)
        self.backgroundColor = data.get("backgroundColor", TCOLOR)
        self.sliderColor = data.get("sliderColor", (200,200,200,100))
        self.onChangeMethod = data.get("onChange", self.change)
        self.percentPixels = self.width / 100.0
        self.update()

    def change(self, data=0):
        print(f"[INFO] Slider @: {self.percent}")

    def onChange(self):
        self.onChangeMethod(self.percent)
    
    def setPercent(self, percent):
        self.percent = percent
    
    def refresh(self):
        self.percentPixels = self.width / 100.0
        self.surface = pg.Surface((self.width, self.height), pg.SRCALPHA)
    
    def draw(self, largeSurface):
        self.surface.fill(self.backgroundColor)
        pg.draw.rect(self.surface, self.color,[0, self.height / 4, self.width, self.height/2])
        #pg.draw.rect(self.surface, self.sliderColor, [(self.percent * self.percentPixels) -5, 0, 10, self.height])
        sliderPos = self.percent
        if(sliderPos > 98):
            sliderPos = 98
        elif (sliderPos < 10):
            sliderPos = 10
        pg.draw.circle(self.surface, self.sliderColor, (int(sliderPos * self.percentPixels) -5, int(self.height / 2)), int(self.height/ 2))
        super(Slider, self).draw(largeSurface)

    def check_click(self, mouseEvent, offsetX=0, offsetY=0):
        isClicked = super(Slider, self).check_click(mouseEvent, offsetX, offsetY)
        if isClicked:
            self.percent = ((mouseEvent.pos[0] - offsetX - self.position[0])) / self.percentPixels
            if self.percent > 100.0:
                self.percent = 100.0
            if self.percent < 0:
                self.percent = 0.0
            self.onChange()
        return isClicked
    
    def add(self, amount):
        self.percent += amount
        if self.percent > 100.0:
            self.percent = 100.0
        if self.percent < 0:
            self.percent = 0.0
        self.onChange()
    
    def getPercent(self):
        return self.percent

class Spinner(Component):
    def __init__(self, position, **data):
        super(Spinner, self).__init__(position, **data)
        self.angle = 0
        self.surface = pg.image.load(spinner_img).convert_alpha()
        self.angle = 0
        self.pos = self.position
        self.old_surface = self.surface

    def update(self):
        self.angle += 10
        self.surface = pg.transform.rotate(self.old_surface, -self.angle)
        self.position = (self.pos[0] - (self.surface.get_width()/ 2), self.pos[1] - (self.surface.get_height()/ 2))
