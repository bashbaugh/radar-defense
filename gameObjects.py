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
grey = (127, 127, 127)
skyBlue = (137, 188, 255)
antimissileOrange = (255, 144, 0)

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
            for i in range(self.game.numMissiles):
                self.game.missiles.append(Missile(self.game))
            self.enabled = False
            utils.text(self.game.screen, "START!", 280, 240, 45)
            
        
    def checkForConnection(self):
        utils.text(self.game.screen, "Please turn knob to position 1.", 50, 170, 45)
        utils.text(self.game.screen, "And turn off all shields.", 65, 240, 45)
        for shield in self.game.interface.shieldOn:
                if shield != False:
                    return
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
        self.tripTime = random.randint(50, 110)
        self.posx, self.posy = self.generateOrigin()
        #self.camPosition = (0,0)
        self.height = random.randint(1, 4)
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
            self.game.energy.progTimer = 0
            self.game.antimissile.enabled = False
            self.explosionSize += 10;
            pygame.draw.circle(self.game.screen, white, (320, 240), self.explosionSize)
            if self.explosionSize >= 700:
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
            self.radarSurf = pygame.transform.rotate(self.originalRadarSurf, -rotation)
            
            if self.game.interface.radarOn:
                pygame.draw.polygon(self.game.screen, radarGreen, self.radar_sector_vertices[self.scan_sector - 1], 3)
            
                for missile in self.game.missiles:
                    if missile.enabled:
                        missilePos = Point(missile.posx, missile.posy)
                        polygon = Polygon(self.radar_sector_vertices[self.scan_sector - 1])
                        if polygon.contains(missilePos):
                            pygame.draw.circle(self.game.screen, radarGreen, (int(missile.posx), int(missile.posy)), 2)
        
        self.game.screen.blit(self.radarSurf, (320 - 35, 220 - 30))

class AntiMissileSystem:
    cameraPositions = [(64, 500), (128, 500), (192, 500), (256, 500), (320, 500),\
        (384, 500), (448, 500), (512, 500),(64, 557), (128, 557), (192, 557),\
        (256, 557), (320, 557), (384, 557), (448, 557), (512, 557)]
    cameraWidth = 56
    cameraHeight = 49
    
    def __init__(self, game):
        self.game = game
        self.enabled = False
        self.antiMissilesRemaining = self.game.numMissiles
        self.antiMissileStage = 0
        self.antiMissileLoop = False
        self.currentCam = 0
        self.antiMissilex = 0
        self.antiMissiley = 0
        self.xpos = 1
        self.ypos = 1
        self.firetimer = 0
        self.FIRE = False
    
    def update(self):
        for missile in self.game.missiles:
            if missile.enabled:
                dist = utils.dist(missile.posx, missile.posy, 320, 240)
                if dist <= 100:
                    missileAngle = int(utils.angleBetween(320, 240, missile.posx, missile.posy))
                    if missileAngle < 0:
                        missileAngle = 360 - abs(missileAngle)
                    #print(missileAngle)
                    missileSector = int(missileAngle / 45)
                    offsetx = int(missileAngle % 45) + 10
                    offsety = 5
                    if missile.height == 1:
                        offsety = 15
                    if missile.height == 2:
                        offsety = 30
                    if missile.height == 3:
                        missileSector += 8
                        offsety = 15
                    if missile.height == 4:
                        missileSector += 8
                        offsety = 30
                    mx = self.cameraPositions[missileSector][0] + offsetx
                    my = self.cameraPositions[missileSector][1] + offsety
                    ms = int(dist / 20 * -1 + 7)
                    pygame.draw.circle(self.game.screen, red, (mx, my), ms)
                    if self.FIRE:
                        if utils.pointWithinCircle(mx, my, self.antiMissilex, self.antiMissiley, 8):
                            missile.enabled = False
                            self.game.missiles.append(Missile(self.game))
                            pygame.draw.circle(self.game.screen, white, (mx, my), 15)
                            cancelAntiMissile()
                        self.FIRE = False
                    
        if self.antiMissileLoop:
            self.antiMissile()
            
            
        if self.game.interface.antiMissile and self.antiMissilesRemaining > 0:
            self.antiMissileLoop = True
            self.game.interface.radarOn = False
            
    def cancelAntiMissile(self):
            self.antiMissileLoop = False
            self.antiMissileStage = 0
            self.antiMissilex = 0
            self.antiMissiley = 0
            self.xpos = 1
            self.ypos = 1
            self.fireTimer = 0

    def antiMissile(self):
            
        if self.game.interface.radarOn == True:
            self.cancelAntiMissile()
            return
        if self.antiMissileStage == 0:
            if self.game.interface.antiMissile:
                self.antiMissileStage = 1
                return
            self.AMrect = pygame.Rect((self.cameraPositions[self.currentCam][0] + 4, self.cameraPositions[self.currentCam][1] + 4), (self.cameraWidth, self.cameraHeight))
            pygame.draw.rect(self.game.screen, green , self.AMrect, 2)            
            if self.currentCam == 15:
                self.currentCam = 0
            else:
                self.currentCam += 1
                
        if self.antiMissileStage == 1:
            if self.game.interface.antiMissile:
                self.antiMissileStage = 2
            pygame.draw.rect(self.game.screen, green , self.AMrect, 2)
            self.antiMissilex= self.cameraPositions[self.currentCam-1][0] + 15
            self.ypos = 1 if self.ypos == 2 else 2
            self.antiMissiley = self.cameraPositions[self.currentCam-1][1] + self.ypos * 15
            pygame.draw.circle(self.game.screen, antimissileOrange, (self.antiMissilex, self.antiMissiley), 8, 1)
            
        if self.antiMissileStage == 2:
            if self.game.interface.antiMissile: 
                self.xpos  += 1
                self.fireTimer = 0
            else:
                self.fireTimer += self.game.deltatime
            if self.xpos >= 12: self.xpos = 1
            pygame.draw.rect(self.game.screen, green , self.AMrect, 2)
            self.antiMissilex = self.cameraPositions[self.currentCam-1][0] + self.xpos * 5
            pygame.draw.circle(self.game.screen, antimissileOrange, (self.antiMissilex, self.antiMissiley), 8, 1)
            if self.fireTimer >= 2000:
                self.FIRE = True
                self.antiMissilesRemaining -= 1
                self.game.energy.energy -= 3
                self.antiMissileStage = 3

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
        
        self.progress = floor(self.progTimer / 22200)
        if self.progress >= 10:
            self.game.gameover.won = True
        utils.text(self.game.screen, "{0}/10".format(str(self.progress).split(".")[0]), 10, 10, 25)
        utils.text(self.game.screen, "{0}x anti-Missiles".format(str(self.game.antimissile.antiMissilesRemaining)), 500, 460, 20)
        
        
        
        
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
        self.game = game
        
    def update(self):
        # Sector Lines:
        pygame.draw.line(self.screen, white, (320, 130), (320, 5))#top
        pygame.draw.line(self.screen, white, (210, 240), (80, 240))#left
        pygame.draw.line(self.screen, white, (430, 240), (560, 240))#right
        pygame.draw.line(self.screen, white, (320, 330), (320, 475))#bottom
        pygame.draw.line(self.screen, white, (410, 150), (500, 60))#top right
        pygame.draw.line(self.screen, white, (390, 310), (500, 420))#bottom right
        pygame.draw.line(self.screen, white, (230, 150), (140, 60))#top left
        pygame.draw.line(self.screen, white, (250, 310), (140, 420))#bottom left
        
        #bottom/top divider line:
        pygame.draw.line(self.screen, white, (10, 485), (630, 485), 2)
        
        #camera divider lines:
        for i in range(1, 10):
            pygame.draw.line(self.screen, grey, (64*i, 500), (64*i, 620))
        pygame.draw.line(self.screen, grey, (64, 557), (576, 557))
        
        #missile cam sky color:
        for camera in self.game.antimissile.cameraPositions:
            rect = pygame.Rect((camera[0] + 4, camera[1] + 4), (self.game.antimissile.cameraWidth, self.game.antimissile.cameraHeight))
            pygame.draw.rect(self.screen, skyBlue , rect)

        
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
            print("Your base was destroyed. :(")
        if self.won:
            for o in self.game.gameObjects:
                o.enabled = False
            self.enabled = True
            self.game.interface.enabled = True
            utils.text(self.game.screen, "You Won", 160, 160, 80, green)
            print("Your engineers fixed your power generator. :)")
            
