import pygame
from time import sleep

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

class Interface:
    def __init__(self, game):
        self.quit = False
        self.events = None
        self.enabled = True
        self.keyboard = True
        self.eventHandler = None
        self.radarPosition = 1
    
    def update(self):
        if self.keyboard:
            self.events = self.eventHandler.get()
            for event in self.events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.radarPosition = constrain(self.radarPosition - 1, 1, 8)
                    if event.key == pygame.K_RIGHT:
                        self.radarPosition = constrain(self.radarPosition + 1, 1, 8)
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.QUIT):
                    self.quit = True
                 #if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                   # self.quit = True
    def connectToController(self):
        #sleep(1)
        self.keyboard = True
        return False


