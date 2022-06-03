import math
import pygame
import neuralnet as nn
import numpy as np

INPUT_SIZE = 6
HIDDEN_SIZE = 4
OUTPUT_SIZE = 2


class Player():
    def __init__(self, brain = None):
        pygame.sprite.Sprite.__init__(self)
        self.playerRight = pygame.transform.scale(pygame.image.load("assets/right.png"), (80,80)).convert_alpha()        # Facing Right
        self.playerRight_1 = pygame.transform.scale(pygame.image.load("assets/rightSit.png"), (80,80)).convert_alpha()   # Facing Right while launching
        self.playerLeft = pygame.transform.scale(pygame.image.load("assets/left.png"), (80,80)).convert_alpha()         # Facing Left
        self.playerLeft_1 = pygame.transform.scale(pygame.image.load("assets/leftSit.png"), (80,80)).convert_alpha()     # Facing Left while launching
        self.x = 300            # Current X position
        self.y = 550              # Current Y position
        self.startY = 300
        self.direction = 0          # direction facing; 0 is right; 1 is left
        self.xvel = 0
        self.ai = True
        if brain is None: self.ai = False
        self.brain = brain
        self.jump = 0
        self.gravity = 0
        self.fitness = 0
        self.alive = True

    
    def move(self, decision = None):
        if self.jump == 0:        
            self.gravity += 0.5
            self.y += self.gravity
            self.startY -= self.gravity

        elif self.jump > 0:
            self.jump -= 1
            self.y -= self.jump
            
            self.startY += self.jump
        
        # print(self.startY)

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            if (self.ai == True):
                self.ai = False
            else:
                self.ai = True

        if (self.ai == True):
            if (decision == 0):
                if self.xvel < 10:
                    self.xvel += 1
                    self.direction = 0

            elif (decision == 1):
                if self.xvel > -10:
                    self.xvel -= 1
                self.direction = 1
            elif (decision == 2):
                if self.xvel > 0:
                    self.xvel -= 1
                elif self.xvel < 0:
                    self.xvel += 1
        else:
            if key[pygame.K_RIGHT]:
                if self.xvel < 10:
                    self.xvel += 1
                    self.direction = 0

            elif key[pygame.K_LEFT]:
                if self.xvel > -10:
                    self.xvel -= 1
                self.direction = 1
            else:
                if self.xvel > 0:
                    self.xvel -= 1
                elif self.xvel < 0:
                    self.xvel += 1
        
        self.x += self.xvel
        
        # When at the edge of the screen go to the other side
        if self.x > 650:
            self.x = -50
        elif self.x < -50:
            self.x = 650
    
    def getNextPos(self, decision):
        if self.jump == 0:
            gravity = self.gravity + 0.5
            yPos = self.y + gravity

        elif self.jump > 0:
            jump = self.jump - 1
            yPos = self.y - jump

        xvel = self.xvel
        if (self.ai == True):
            if (decision == 0):
                if xvel < 10:
                    xvel += 1

            elif (decision == 1):
                if xvel > -10:
                    xvel -= 1
                    
            elif (decision == 2):
                if xvel > 0:
                    xvel -= 1
                elif xvel < 0:
                    xvel += 1
        xPos = self.x + 1*xvel
        
        # When at the edge of the screen go to the other side
        if xPos > 650:
            xPos = -50
        elif xPos < -50:
            xPos = 650
        return (xPos,yPos)
        
    # Ai Part
    def think(self, platforms, monsters):
        coordinatesUp = self.getPlatformAbove(platforms)
        coordinatesDown = self.getPlatformBelow(platforms)
        inputs = [0 for i in range(INPUT_SIZE)]
        vision = self.look(platforms)
        
        inputs[0] = vision[1]
        inputs[1] = vision[2]
        inputs[2] = vision[3]

        #inputs.append(self.x/600)                   # Player X value
        xup=coordinatesUp - 2*self.xvel -self.x
        xdown = coordinatesDown - 2*self.xvel -self.x
        inputs[3] = xup%600 if xup%600<abs(xup%600-600) else xup%600-600         # X value of platform above
        inputs[4] = xdown%600 if xdown%600<abs(xdown%600-600) else xdown%600-600         # X value of platform below
        inputs[5] = monsters[0].x + monsters[0].vel if len(monsters) !=0  else 0
        output = self.brain.feedForward(inputs).tolist()     

        index = output.index(max(output))
        if index == 2:
            index = np.random.randint(3)
        return index

    # Retrieve X value of platform above player
    def getPlatformAbove(self,platforms):
        if self.jump > 5: # moving up, above the player
            for p in platforms:
                if (self.startY-80 < p.startY): # above the player
                    if (p.kind != 2): # not red 
                        if (abs(p.x + p.vel - self.x) < 400): # not too far
                            return (p.x + p.vel)
        else:# falling, below the player
            maxX = 0
            for p in platforms:
                if (self.startY-80 > p.startY):
                    if (p.kind != 2):
                        if (abs(p.x + p.vel - self.x) < 300):
                            maxX = p.x + p.vel
            return maxX
    
    def getPlatformsPossible(self,platforms,candidateNum):
        returnPlatforms = []
        if self.jump > 5: # moving up, above the player
            for p in platforms:
                if (self.startY < p.startY): # above the player
                    if (p.kind != 2): # not red 
                        if (abs(p.x + p.vel - self.x) < 400): # not too far
                            returnPlatforms.append(p.x + p.vel)
                            if len(returnPlatforms)==candidateNum: break
            return returnPlatforms
        else:# falling, below the player
            for p in platforms:
                if (self.startY > p.startY):
                    if (p.kind != 2):
                        if (abs(p.x + p.vel - self.x) < 400):
                            returnPlatforms.append(p.x + p.vel)
            if len(returnPlatforms)==0: return[0]
            return returnPlatforms[-1:-1-candidateNum:-1]

    def getMonsterAbove(self,monsters):
        if len(monsters)==0: return 999
        if self.jump > 5: # moving up, above the player
            for p in monsters:
                if (self.startY < p.startY) and (p.startY - self.startY < 300):
                    if (p.kind != 2):
                        return (p.x + p.vel)
                else: return 999 # does not consider it because too far
        else:# falling, below the player
            maxX = 0
            for p in monsters:
                if (self.startY > p.startY):
                    if (p.kind != 2):
                        maxX = p.x + p.vel
            return maxX
            
    # Retrieve X value of platform below player
    def getPlatformBelow(self,platforms):
        maxX = 0
        for p in platforms:
            if (self.startY > p.startY):
                if (p.kind != 2):
                    if (abs(p.x + p.vel - self.x) < 300): # not too far
                        maxX = p.x + p.vel
        return maxX

    def fitnessExpo(self):
        self.fitness = self.fitness**2

    # Player looks from 8 directions to find platforms
    def look(self, platforms):
        vision = [0, 0, 0, 0]

        for p in platforms:
            rect = pygame.Rect(p.x , p.y, p.green.get_width(), p.green.get_height())
            
            up = pygame.Rect(self.x+ 50, self.y, 1, 800)
            down = pygame.Rect(self.x + 50, self.y-800, 1, 800)
            left = pygame.Rect(self.x-600, self.y +50, 600, 1)
            right = pygame.Rect(self.x, self.y +50, 600, 1)

            if (rect.colliderect(up) and p.kind != 2):
                vision[0] = 1

            if (rect.colliderect(down) and p.kind != 2):
                vision[1] = 1

            if (rect.colliderect(left) and p.kind != 2):
                vision[2] = 1

            if (rect.colliderect(right) and p.kind != 2):
                vision[3] = 1

        return vision

    def clone(self):
        cloneBrain = self.brain.clone()
        clone = Player(cloneBrain)
        return clone