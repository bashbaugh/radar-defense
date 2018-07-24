import pygame
from time import sleep
import utils

class Interface:
    def __init__(self, game):
        self.quit = False
        self.events = None
        self.enabled = True
        self.keyboard = False
        self.eventHandler = None
        self.radarPosition = 1
        self.radarOn = False
        self.shieldOn = [False, False, False, False, False, False, False, False, False]
    
    def update(self):
        if self.keyboard:
            self.events = self.eventHandler.get()
            for event in self.events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.radarPosition = utils.constrain(self.radarPosition - 1, 1, 8)
                    if event.key == pygame.K_RIGHT:
                        self.radarPosition = utils.constrain(self.radarPosition + 1, 1, 8)
                    if event.key == pygame.K_SPACE:
                        self.radarOn = not self.radarOn
                    if event.key == pygame.K_1:
                        self.shieldOn[1] = not self.shieldOn[1]
                    if event.key == pygame.K_2:
                        self.shieldOn[2] = not self.shieldOn[2]
                    if event.key == pygame.K_3:
                        self.shieldOn[3] = not self.shieldOn[3]
                    if event.key == pygame.K_4:
                        self.shieldOn[4] = not self.shieldOn[4]
                    if event.key == pygame.K_5:
                        self.shieldOn[5] = not self.shieldOn[5]
                    if event.key == pygame.K_6:
                        self.shieldOn[6]= not self.shieldOn[6]
                    if event.key == pygame.K_7:
                        self.shieldOn[7] = not self.shieldOn[7]
                    if event.key == pygame.K_8:
                        self.shieldOn[8] = not self.shieldOn[8] 
                    
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.QUIT):
                    self.quit = True
                
    def connectToController(self):
        #sleep(1)
        self.keyboard = True


