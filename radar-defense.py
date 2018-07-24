# Radar Defense game
#
#By Benjamin A.

import pygame
from time import sleep

from interface import Interface
import utils
from gameObjects import *

        
class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.init()
        self.gameObjects = []
        self.gamestart = GameStart(self)
        self.radar = Radar(self)
        self.interface = Interface(self)
        self.bg = Background(self)
        self.energy = Energy(self)
        self.shield = Shield(self)
        self.gameover = GameOver(self)
        self.interface.eventHandler = pygame.event
        self.gameObjects.append(self.interface)
        self.gameObjects.append(self.energy)
        self.gameObjects.append(self.bg)
        self.gameObjects.append(self.gameover)
        self.gameObjects.append(self.radar)
        self.gameObjects.append(self.shield)
        self.deltatime = 0
        self.gameObjects.append(self.gamestart)
        
        done = False
        self.clock.tick()
        while not done:
            self.deltatime = self.clock.tick()
            #print(self.deltatime)
            #self.deltatime = pygame.time.Clock.get_time()
            self.screen.fill((000, 000, 000))
            for o in self.gameObjects:
                if o.enabled:
                    o.update()
                    #o.render()
            done = self.interface.quit
        
            pygame.display.flip()
            
        self.quitgame
    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        #utils.screen = self.screen
        pygame.mouse.set_visible(False);
        pygame.display.set_caption("Radar Defense Game")
    
    def quitgame(self):
        pygame.quit()
        
print("----------------\n Radar Defense\n----------------\n\nBy Benjamin A.")
sleep(1)
game = Game()
        

