#import pygame
from math import sqrt

def circle_intersection(c1,c2):
    x1,y1,r1 = c1
    x2,y2,r2 = c2

    dx,dy = x2-x1, y2-y1
    d = sqrt(dx*dx+dy*dy)
    if d > r1+r2:
        return None
    if d < abs(r1-r2):
        return None

    a = (r1*r1-r2*r2+d*d) /(2*d)
    h = sqrt(r1*r1-a*a)
    xm = x1 + a * dx/d
    ym = y1 + a * dy/d
    xs1 = xm + h * dy/d
    xs2 = xm - h * dy/d
    ys1 = ym - h * dx/d
    ys2 = ym + h * dx/d

    return (int(xs1),int(ys1)), (int(xs2), int(ys2))


def hexagon(x,y,radius,p=1):
    if p == 1:
        p1,p2 = circle_intersection((x,y-radius,radius),(x,y,radius))
        p3, p4 =circle_intersection((x,y,radius), (x,y+radius,radius))
        return [[p1[0],p1[1]],[x,y-radius],[p2[0],p2[1]],[p4[0],p4[1]],[x,y+radius],[p3[0],p3[1]]]
    
    elif p == 2:
        p1,p2 = circle_intersection((x-radius, y, radius),(x,y, radius))
        p3,p4 = circle_intersection((x, y, radius), (x+radius, y, radius))
        return [[p1[0],p1[1]],[x-radius, y],[p2[0],p2[1]],[p4[0],p4[1]],[x+radius, y],[p3[0],p3[1]]]
