from __future__ import division
import pygame.font
import pygame.math
import math

pygame.font.init()

def text(screen, text, x, y, size = 50, color = (200, 200, 200), font_type = 'data/fonts/Chrobot.otf'):
    text = str(text)
    font = pygame.font.Font(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

        
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


def lineIntersectsCircle(x1, y1, x2, y2, cx, cy, cr):
    r = cr
    Q = pygame.math.Vector2((cx, cy))
    P1 = pygame.math.Vector2((x1, y1))
    V = pygame.math.Vector2((x2, y2)) - P1
    
    a = V.dot(V)
    b = 2 * V.dot(P1 - Q)
    c = P1.dot(P1) + Q.dot(Q) - 2 * P1.dot(Q) - r**2
    
    disc = b**2 - 4 * a * c
    if disc < 0:
        return False
    
    sqrt_disc = math.sqrt(disc)
    t1 = (-b + sqrt_disc) / (2 * a)
    t2 = (-b - sqrt_disc) / (2 * a)
    
    if not (0 <= t1 <= 1 or 0 <= t2 <= 1):
        return False
    
    t = max(0, min(1, - b / (2 * a)))
    return True

def dist(x1, y1, x2, y2):
    return math.hypot(x1-x2, y1-y2)

def angleBetween(x1, y1, x2, y2):
    deltax = x2 - x1
    deltay = y2 - y1

    angle_rad = math.atan2(deltay,deltax)
    angle_deg = angle_rad*180.0/math.pi

    return angle_deg + 90

def pointWithinCircle(x, y, cx, cy, cr):
    return (x - cx)**2 + (y - cy)**2 < cr**2

    
