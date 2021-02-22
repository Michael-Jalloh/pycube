"""
import pygame,sys
from math import pi, cos, sin, sqrt, atan2
import hexagon

d2r = pi/180


pygame.init()

blue = (0,0,255)

screen = pygame.display.set_mode([400,300],0, 32)

clock = pygame.time.Clock()


def circle_intersection(c1,c2):
    x1,y1,r1 = c1
    x2,y2,r2 = c2

    dx,dy = x2-x1, y2-y1
    d = sqrt(dx*dx+dy*dy)
    if d > r1+r2:
        print('#1')
        return None
    if d < abs(r1-r2):
        print('#3')
        return None
    a = (r1*r1-r2*r2+d*d)/(2*d)
    h = sqrt(r1*r1-a*a)
    xm = x1 + a*dx/d
    ym = y1 + a*dy/d
    xs1 = xm + h*dy/d
    xs2 = xm - h*dy/d
    ys1 = ym - h*dx/d
    ys2 = ym + h*dx/d

    return (int(xs1), int(ys1)), (int(xs2), int(ys2))


running = True
while running:
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((54,54,54))
    tscreen = pygame.Surface((480,320),pygame.SRCALPHA)
    tscreen.fill((54,54,54))
    #tscreen.set_alpha(128)
    #pygame.draw.polygon(tscreen,blue, [[100,100],[0,200],[200,200]])
    #pygame.draw.polygon(tscreen,blue+(25,),[[50,50],[70,35],[240,35],[260,50],[260,100],[245,115],[70,115],[50,100]])
    #pygame.draw.polygon(tscreen,(0,0,0),[[50,50],[70,35],[240,35],[260,50],[260,100],[245,115],[70,115],[50,100]],2)
    #pygame.draw.polygon(tscreen, (0,0,0),[[50,50],[75,25],[100,50],[100,100],[75,125],[50,100]],2)
    #pygame.draw.polygon(tscreen, blue+(25,),[[50,50],[75,25],[100,50],[100,100],[75,125],[50,100]])
    #draw_ngon(screen, blue, 6, 100,[100,100])
    #screen.blit(tscreen,(0,0))
    pygame.draw.circle(tscreen, (255,255,255), [125,125],25,2)
    pygame.draw.rect(tscreen, (255,255,255), [100,100, 50, 50],2)
    #pygame.draw.circle(screen, (255,255,255), [100,100+50],50,2)
    hex1 = hexagon.hexagon(100,100,10)
    hex2 = hexagon.hexagon(200,200, 10)
    #pygame.draw.line(screen, (255,255,255), [int(p1[0]),int(p1[1])],[int(p2[0]),int(p2[1])],2)
    #pygame.draw.line(screen,(255,255,255), [int(p3[0]), int(p3[1])],[int(p4[0]), int(p4[1])],2)
    

    pygame.draw.polygon(tscreen, (255,255,255),hex1, 1)
    #pygame.draw.polygon(tscreen, (200,200,200), hex2)
    pygame.draw.line(tscreen, (255,0,0), hex2[0],hex2[0],10)
    pygame.draw.line(tscreen, (0,255,0), hex2[1],hex2[1],10)
    pygame.draw.line(tscreen, (0,0,255), hex2[2],hex2[2], 10)
    pygame.draw.line(tscreen, (255,255,255), hex2[3],hex2[3], 10)
    pygame.draw.line(tscreen, (200,200,0), hex2[4], hex2[4], 10)
    pygame.draw.line(tscreen, (0,0,0), hex2[5], hex2[5], 10)
    screen.blit(tscreen,(0,0))
    pygame.display.flip()
    
pygame.quit()

from time import sleep

def counter():
    count = 100
    while count <100:
        count += 1
        sleep(0.5)
    return count 


pygame.init()

blue = (0,0,255)

screen = pygame.display.set_mode([400,300],0, 32)

clock = pygame.time.Clock()

img = pygame.image.load("exported/spinner.png").convert_alpha()

angle = 0
while True:
    angle += 10
    screen.fill((0,50,0))
    mx, my = pygame.mouse.get_pos()
    img_copy = pygame.transform.rotate(img, -angle)
    screen.blit(img_copy, (mx - int(img_copy.get_width() / 2), my - int(img_copy.get_height() / 2)))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    pygame.display.update()
    clock.tick(60)

import os

print("Starting Gedit")
os.popen("gedited")
print("Done")"""

import pygame
pygame.init()


SIZE = WIDTH, HEIGHT = (1024, 720)
FPS = 30
screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
clock = pygame.time.Clock()


def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


text = "This is a really long sentence with a couple of breaks. Sometimes it will break even if there isn't a break " \
       "in the sentence, but that's because the text is too long to fit the screen.\nIt can look strange sometimes.\n" \
       "This function doesn't check if the text is too high to fit on the height of the surface though, so sometimes " \
       "text will disappear underneath the surface"
font = pygame.font.SysFont('Arial', 64)

while True:

    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill(pygame.Color('white'))
    blit_text(screen, text, (20, 20), font)
    pygame.display.update()