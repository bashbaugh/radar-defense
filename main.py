import pygame
from game import *

def main():
    done = False
    while not done:
        for o in gameObjects:
            o.update()
            o.draw()
        
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        done = True
        
        pygame.display.flip()
