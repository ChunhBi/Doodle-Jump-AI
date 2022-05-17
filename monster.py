import pygame
import random


class Monster():

    def __init__(self):
        self.kind = 0
        self.blackhole = pygame.transform.scale(pygame.image.load("assets/blackhole.png"), (100, 100)).convert_alpha()
        self.moveMonster_1 = pygame.transform.scale(pygame.image.load("assets/monster_1.png"), (70, 70)).convert_alpha()
        self.moveMonster_2 = pygame.transform.scale(pygame.image.load("assets/monster_2.png"), (70, 70)).convert_alpha()
        self.x = random.randint(0, 500)
        self.originX = self.x
        self.y = 0
        self.startY = -100  # Actual y
        self.monsterDirection = 0

    def getKind(self, score):
        chance = random.randint(0, 100)
        if (score < 200 ):
            self.kind =2
        elif (score < 1500 ):
            if (chance < 2):
                self.kind = 0
            elif (chance < 4):
                self.kind = 1
            else:
                self.kind = 2

        elif (score < 2500):
            if (chance < 3):
                self.kind = 0
            elif (chance < 6):
                self.kind = 1
            else:
                self.kind = 2

        else:
            if (chance < 4):
                self.kind = 0
            elif (chance < 8):
                self.kind = 1
            else:
                self.kind = 2

    def monsterMovement(self, score):
        max_x = self.originX + 50
        min_x = self.originX - 50
        x = 0
        if (score < 2500):
            vel = 5
        else:
            vel = 8

        if (self.monsterDirection > 0):
            x += vel
            self.x += x
            if (self.x >= 600 - self.moveMonster_1.get_width() or self.x >= max_x):
                self.monsterDirection = 0
        else:
            self.x -= vel

            if (self.x <= 0 or self.x <= min_x):
                self.monsterDirection = 1
