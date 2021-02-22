from os import path
from redis import Redis
from .utils import *

# Screen settings
WIDTH = 480
HEIGHT = 320
SCREEN_WIDTH = 459
SCREEN_HEIGHT = 239
FPS = 30


# Color Setup
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ACCENT = (100, 100, 200)
WARNING = (250, 160, 45)
ERROR = (250, 50, 50)
RED = (255, 0 ,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = (33, 37, 43) #(43, 45, 87) # (17, 18, 35) #
TCOLOR = (157, 165, 181)
MAGENTA = (255, 0, 255)


# Directory Setup
directory = path.dirname(__file__)
resources_dir = path.join(directory,'resources')
icon_dir = path.join(resources_dir, 'icons')
font_dir = path.join(resources_dir, 'fonts')
image_dir = path.join(resources_dir, "images")

# images
spinner_img = path.join(image_dir, "spinner.png")
file_img = path.join(image_dir, "file.png")
folder_img = path.join(image_dir, "folder.png")

# Icon path
FONTAWESOME = get_icon(icon_dir, 'fontawesome')

redisConnection = Redis()