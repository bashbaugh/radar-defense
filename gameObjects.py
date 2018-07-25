import utils
import pygame
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from math import floor
import random
import interface
from time import time

white = (255, 255, 255)
radarGreen = (58, 168, 8)
shieldYellow = (255, 216, 0)
red = (255, 0, 0)
green = (0, 255, 0)

class GameStart:
    def __init__(self, game):
        self.enabled = True
        self.game = game
        self.connectTimer = 0
        self.connectionSuccess = False
        #self.gameStarted = False
    
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
            for o in self.game.gameObjects:
                o.enabled = True
            self.enabled = False
            
        
    def checkForConnection(self):
        utils.text(self.game.screen, "Please turn knob to position 1.", 20, 200, 45)
        if self.game.interface.radarPosition == 1:
            self.connectionSuccess = True
        
class Missile:
    
    def __init__(self, game):
        self.shields = []
        self.game = game
        self.enabled = True
        self.explode = False
        self.explosionSize = 0
        self.game.gameObjects.append(self)
        self.tripTime = random.randint(40, 100)
        self.posx, self.posy = self.generateOrigin()
        self.targetx = 320
        self.targety = 240
        self.targetthreshold = 10
        self.shieldthreshold = 5
        self.xdist = self.targetx - self.posx
        self.ydist = self.targety - self.posy
    
    def update(self):
        if self.posx <= 330 and self.posx >= 310 and self.posy <= 250 and self.posy >= 230:
            self.explode = True
        
        if self.explode:
            self.explosionSize += 10;
            pygame.draw.circle(self.game.screen, white, (320, 240), self.explosionSize)
            if self.explosionSize >= 500:
                self.game.gameover.lost = True
        else:
            self.missileLoop()
            
        
    def missileLoop(self):
        #deltaSeconds = self.game.deltatime / 1000
            fps = self.game.fps
            try:
                movex = self.xdist / fps / self.tripTime
                movey = self.ydist / fps / self.tripTime
            except:
                movex = 0
                movey = 0
            self.posx += movex
            self.posy += movey
            
            shields = self.game.shield.shield_locations
            for i in range(8):
                if self.game.shield.shieldsOn[i+1]:
                    if utils.lineIntersectsCircle(shields[i][0][0], shields[i][0][1],\
                    shields[i][1][0], shields[i][1][1], int(self.posx), int(self.posy), 2):
                        self.enabled = False
                        pygame.draw.circle(self.game.screen, white, (int(self.posx), int(self.posy)), 5)
                        self.game.missiles.append(Missile(self.game))
        
        
    def generateOrigin(self):
        quadrant = random.randint(1,4)
        if quadrant == 1:
            x = random.randint(130, 610)
            y = 10
        if quadrant == 2:
            x = 560
            y = random.randint(20, 460)
        if quadrant == 3:
            x = random.randint(130, 610)
            y = 470
        if quadrant == 4:
            x = 80
            y = random.randint(20, 460)
        return x, y

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
        if self.game.energy.energyAvailable:
            self.scan_sector = self.game.interface.radarPosition
            rotation = (self.scan_sector * (360/8)) - 22
            
            if self.game.interface.radarOn:
                pygame.draw.polygon(self.game.screen, radarGreen, self.radar_sector_vertices[self.scan_sector - 1], 3)
            
                for missile in self.game.missiles:
                    if missile.enabled:
                        missilePos = Point(missile.posx, missile.posy)
                        polygon = Polygon(self.radar_sector_vertices[self.scan_sector - 1])
                        if polygon.contains(missilePos):
                            pygame.draw.circle(self.game.screen, radarGreen, (int(missile.posx), int(missile.posy)), 2)
        
        radarSurf = pygame.transform.rotate(self.originalRadarSurf, -rotation)
        self.game.screen.blit(radarSurf, (320 - 35, 220 - 30))


class Energy:
    def __init__(self, game):
        self.enabled = False
        self.game = game
        self.energy = 100
        self.progress = 0
        self.timer = 0
        self.progTimer = 0
        self.energyAvailable = True
        
    def update(self):
        deltaT = self.game.deltatime
        self.timer += deltaT
        self.progTimer += deltaT
        if self.game.interface.radarOn:
            self.timer += 2 * deltaT
        for shield in self.game.interface.shieldOn:
            if shield:
                self.timer += deltaT
        self.energy -= self.timer / 5000
        if self.timer >= 5000: 
            self.timer = 0
        if self.energy <= 0:
            self.energy = 0
            self.energyAvailable = False
        utils.text(self.game.screen, "Energy {0}%".format(str(self.energy)), 510, 10, 25)
        
        self.progress = floor(self.progTimer / 30200)
        if self.progress >= 10:
            self.game.gameover.won = True
        utils.text(self.game.screen, "{0}/10".format(str(self.progress).split(".")[0]), 10, 10, 25)
        
        
        
class Shield:
    shield_locations = [[(320, 130), (410, 150)], [(410, 150), (430, 240)],\
        [(430, 240), (390, 310)], [(390, 310), (320, 330)], [(320, 330), (250, 310)],\
        [(250, 310), (210, 240)], [(210, 240), (230, 150)], [(230, 150), (320, 130)]]
    def __init__(self, game):
        self.enabled = False
        self.game = game
        self.shieldsOn = [False, False, False, False, False, False, False, False, False]
        
    def update(self):
        if self.game.energy.energyAvailable:
            self.shieldsOn = self.game.interface.shieldOn
            for i in range(8):
                if self.shieldsOn[i + 1]:
                    pygame.draw.line(self.game.screen, shieldYellow,\
                        self.shield_locations[i][0], self.shield_locations[i][1])
        else:
            self.shieldsOn = [False, False, False, False, False, False, False, False, False]

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
        if self.won:
            for o in self.game.gameObjects:
                o.enabled = False
            self.enabled = True
            self.game.interface.enabled = True
            utils.text(self.game.screen, "You Won", 160, 160, 80, red)
            
