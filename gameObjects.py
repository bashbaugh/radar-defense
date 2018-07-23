import utils
import pygame
import interface
from time import time

white = (200, 200, 200)

class LoadingScreen:
    def __init__(self, game):
        self.enabled = True
        self.game = game
        self.connectFailed = False
    
    def update(self):
        if not self.connectFailed:
            utils.text(self.game.screen, "Connecting to controller...", 90, 200, 45)
            self.connectFailed = not interface.connectToController()
        else:
            utils.text(self.game.screen, "Unable to connect to controller.", 30, 200, 45)
            utils.text(self.game.screen, "Using keyboard input.", 110, 250, 45)
            self.enabled = False
            self.game.radar.enabled = True
            
        
    def render(self):
        pass
    
class Radar:
    def __init__(self, game):
        self.game = game
        self.rotation = 0
        self.scan_sector = 1
        self.enabled = True
        self.originalRadarSurf = pygame.image.load("data/images/radar.png").convert()
        self.starttime = time()

    def update(self):
        rotation = (self.game.interface.radarPosition * (360/8)) - 22
        radarSurf = pygame.transform.rotate(self.originalRadarSurf, -rotation)
        rect = radarSurf.get_rect()
        #rect.center = (320, 240)
        #self.radarSurf = pygame.transform.rotate(self.radarSurf, 10)
        self.game.screen.blit(radarSurf, (320 - 35, 220 - 30))

    def render(self):
        pass
    
class Background:
    def __init__(self, game):
        self.enabled = True
        self.screen = game.screen
        
    def update(self):
        pygame.draw.line(self.screen, white, (320, 130), (320, 0))#top
        pygame.draw.line(self.screen, white, (210, 240), (0, 240))#left
        pygame.draw.line(self.screen, white, (430, 240), (560, 240))#right
        pygame.draw.line(self.screen, white, (320, 330), (320, 480))#bottom
        pygame.draw.line(self.screen, white, (410, 150), (500, 60))#top right
      #  pygame.draw.line(self.screen, white, (320, 150), (320, 0))#bottom right
        #pygame.draw.line(self.screen, white, (320, 150), (320, 0))
        #pygame.draw.line(self.screen, white, (320, 150), (320, 0))
        
