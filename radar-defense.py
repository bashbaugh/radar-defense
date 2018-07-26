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
        self.level = 1
        self.clock = pygame.time.Clock()
        self.initModules()
        self.gameObjects = []
        self.gamestart = GameStart(self)
        self.missiles = []
        self.radar = Radar(self)
        self.interface = Interface(self)
        self.bg = Background(self)
        self.energy = Energy(self)
        self.shield = Shield(self)
        self.antimissile = AntiMissileSystem(self)
        self.gameover = GameOver(self)
        self.interface.eventHandler = pygame.event
        self.gameObjects.append(self.interface)
        self.gameObjects.append(self.energy)
        self.gameObjects.append(self.bg)
        self.gameObjects.append(self.gameover)
        self.gameObjects.append(self.radar)
        self.gameObjects.append(self.antimissile)
        self.gameObjects.append(self.shield)
        self.gameObjects.append(self.gamestart)
        self.deltatime = 0
        self.fps = 0
        self.level = 1
        self.numMissiles = number_of_missiles
        
        
        done = False
        self.clock.tick()
        while not done:
            self.deltatime = self.clock.tick(60)
            self.fps = self.clock.get_fps()
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
    def initModules(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 640))
        #utils.screen = self.screen
        pygame.mouse.set_visible(False);
        pygame.display.set_caption("Radar Defense Game")
    
    def quitgame(self):
        pygame.quit()
        
print("\n----------------\n Radar Defense\n----------------\n\nBy Benjamin A.\n")
print("You are the director of a top secret base. Unfortunately, your power generator broke down today, and some enemies have taken the opportunity to come and attack you with missiles. Without power, you cannot operate your shields, and cannot block the missiles. Luckily, you have several backup supply batteries, but they will only last for so long. Your job is to survive long enough for your engineers to fix the power generator.\n")
number_of_missiles = input("Choose a number of missiles(1=super easy, 2 = easy, 3=normal, 5 = super hard):")
print("\n\n-------- Instructions: --------\nTry to survive as long as you can. the sky is divided into eight sectors, each sector has a shield. Use your shields to block incoming missiles(don't let them get to the radar!). You can turn your radar on to scan different sectors of the sky for missiles - but only have your radar and shields on when neccessary, because they use lots of energy. Your remaining energy is in the top right corner. The top left corner shows the progress of the engineers fixing the power generator. \nThere will always be {0} active missiles in the sky.\n\n".format(number_of_missiles))

pause = raw_input("Press enter to start.")
game = Game()

print("\nGoodbye!\n\n")
        

