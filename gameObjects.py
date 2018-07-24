import utils
import pygame
import interface
from time import time

white = (200, 200, 200)
radarGreen = (58, 168, 8)
shieldYellow = (255, 216, 0)
red = (255, 0, 0)

class GameStart:
    def __init__(self, game):
        self.enabled = True
        self.game = game
        self.connectTimer = 0
        self.connectionSuccess = False
    
    def update(self):
        self.connectTimer += self.game.deltatime
        if (not self.game.interface.keyboard) and (not self.game.interface.controller):
            utils.text(self.game.screen, "Connecting to controller...", 90, 200, 45)
            self.game.interface.connectToController()
        elif self.connectTimer < 2000 and self.game.interface.keyboard:
            utils.text(self.game.screen, "Unable to connect to controller.", 30, 200, 45)
            utils.text(self.game.screen, "Using keyboard input.", 110, 250, 45)
        elif self.connectTimer < 2000 and self.game.interface.controller:
            utils.text(self.game.screen, "Successfuly connected to controller", 10, 200, 40)
        elif self.game.interface.controller and not self.connectionSuccess:
            self.checkForConnection()
        else:
            self.enabled = False
            for o in self.game.gameObjects:
                o.enabled = True
            
        
    def checkForConnection(self):
        utils.text(self.game.screen, "Please turn knob to position 1.", 20, 200, 45)
        if self.game.interface.radarPosition == 1:
            self.connectionSuccess = True
        


class Radar:
    radar_sector_vertices = [((320, 240), (500, 60), (320, 5)),\
        ((320, 240), (500, 60), (560, 240)), \
        ((320, 240), (560, 240), (500, 420)),\
        ((320, 240), (500, 420), (320, 475)),\
        ((320, 240), (320, 475), (140, 420)),\
        ((320, 240), (140, 420), (80, 240)),\
        ((320, 240), (80, 240), (140, 60)),\
        ((320, 240), (140, 60), (320, 5))]
    def __init__(self, game):
        self.game = game
        self.rotation = 0
        self.scan_sector = 1
        self.enabled = False
        self.originalRadarSurf = pygame.image.load("data/images/radar.png").convert()
        self.starttime = time()

    def update(self):
        rotation = (self.game.interface.radarPosition * (360/8)) - 22
        radarSurf = pygame.transform.rotate(self.originalRadarSurf, -rotation)
        if self.game.interface.radarOn:
            pygame.draw.polygon(self.game.screen, radarGreen, self.radar_sector_vertices[self.game.interface.radarPosition - 1], 3)
        self.game.screen.blit(radarSurf, (320 - 35, 220 - 30))

    def render(self):
        pass

class Energy:
    def __init__(self, game):
        self.enabled = False
        self.game = game
        self.energy = 100
        self.timer = 0
        
    def update(self):
        deltaT = self.game.deltatime
        self.timer += deltaT
        if self.game.interface.radarOn:
            self.timer += 2 * deltaT
        for shield in self.game.interface.shieldOn:
            if shield:
                self.timer += deltaT
        self.energy -= self.timer / 5000
        if self.timer >= 5000: self.timer = 0
        utils.text(self.game.screen, "Energy {0}%".format(str(self.energy)), 510, 10, 25)
        if self.energy <= 0:
            self.game.gameover.lost = True
class Shield:
    shield_locations = [[(320, 130), (410, 150)], [(410, 150), (430, 240)],\
        [(430, 240), (390, 310)], [(390, 310), (320, 330)], [(320, 330), (250, 310)],\
        [(250, 310), (210, 240)], [(210, 240), (230, 150)], [(230, 150), (320, 130)]]
    def __init__(self, game):
        self.enabled = False
        self.game = game
        
    def update(self):
        for i in range(8):
            if self.game.interface.shieldOn[i + 1]:
                pygame.draw.line(self.game.screen, shieldYellow,\
                    self.shield_locations[i][0], self.shield_locations[i][1])

class Background:
    def __init__(self, game):
        self.enabled = False
        self.screen = game.screen
        
    def update(self):
        # Lines:
        pygame.draw.line(self.screen, white, (320, 130), (320, 5))#top
        pygame.draw.line(self.screen, white, (210, 240), (80, 240))#left
        pygame.draw.line(self.screen, white, (430, 240), (560, 240))#right
        pygame.draw.line(self.screen, white, (320, 330), (320, 475))#bottom
        pygame.draw.line(self.screen, white, (410, 150), (500, 60))#top right
        pygame.draw.line(self.screen, white, (390, 310), (500, 420))#bottom right
        pygame.draw.line(self.screen, white, (230, 150), (140, 60))#top left
        pygame.draw.line(self.screen, white, (250, 310), (140, 420))#bottom left
        
class GameOver:
    def __init__(self, game):
        self.game = game
        self.enabled = True
        self.lost = False
        self.won = False
    
    def update(self):
        if self.lost:
            for o in self.game.gameObjects:
                o.enabled = False
            self.enabled = True
            self.game.interface.enabled = True
            utils.text(self.game.screen, "You Lost", 160, 160, 80, red)
            
