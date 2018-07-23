import pygame
from time import sleep

from interface import Interface
import utils
from gameObjects import *

        
class Game:
    def __init__(self):
        self.init()
        self.gameObjects = []
        #self.loadingscreen = LoadingScreen(self)
        self.radar = Radar(self)
        self.interface = Interface(self)
        self.bg = Background(self)
        self.interface.eventHandler = pygame.event
        self.gameObjects.append(self.interface)
        self.gameObjects.append(self.bg)
        self.gameObjects.append(self.radar)
        #self.gameObjects.append(self.loadingscreen)
        
        done = False
        while not done:
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
        pygame.display.set_caption("My Game")
    
    def quitgame(self):
        pygame.quit()
        
game = Game()
        

