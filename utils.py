import pygame.font
import math

pygame.font.init()

def text(screen, text, x, y, size = 50, color = (200, 200, 200), font_type = 'data/fonts/Chrobot.otf'):
    text = str(text)
    font = pygame.font.Font(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

        
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

 
def checkCollision(a, b, c, x, y, radius):
    
    dist = ((abs(a * x + b * y + c)) /
            math.sqrt(a * a + b * b))
 
    if (radius == dist):
        return True
    elif (radius > dist):
        return True
    else:
        return False
