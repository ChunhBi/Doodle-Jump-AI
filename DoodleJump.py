import pygame
import numpy as np
import Platform
import neuralnet as nn
import Player
import monster
import ga
import time
import agent

false = False
true = True

W = 600
H = 800
TOTAL = 20

class DoodleState():
    def __init__(self, other = None):
        if other is not None:
            self.platforms = other.platforms
            self.monsters = other.monsters
            self.springs = other.springs
            self.player = other.player
        else:
            self.platforms = []
            self.monsters = []
            self.springs = []
            self.player = None
    
    def updateState(self,platforms,monsters,springs,player):
        self.platforms = platforms
        self.monsters = monsters
        self.springs = springs
        self.player = player


class DoodleJump():
    def __init__(self):
        self.screen = pygame.display.set_mode((W, H))
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 25)
        self.background_image = pygame.image.load('assets/background.png')
        self.camera = 0
        self.startY = -100
        self.generation = 1
        self.time = time.time()

        # score settings
        self.score = 0
        self.scoreCoefficient = 250
        self.difficultyCoefficient = 80

        # three kinds of elements
        self.platforms = []
        self.monsters = []
        self.springs = []
        self.player = None
        self.danger = False  #小怪是否危险

    def playerUpdate(self, player):
        # Camera follow player when jumping
        if player.y - self.camera <= 200:
            # the higher jumping the higher score
            self.score += int((-self.camera - 8) / self.scoreCoefficient)
            self.camera -= 8

    def drawPlayer(self, player):
        # facing right
        if player.direction == 0:
            if player.jump > 0:  # jumping
                self.screen.blit(player.playerRight_1, (player.x, player.y - self.camera))
            else:
                self.screen.blit(player.playerRight, (player.x, player.y - self.camera))
        # facing left
        else:
            if player.jump > 0:  # jumping
                self.screen.blit(player.playerLeft_1, (player.x, player.y - self.camera))
            else:
                self.screen.blit(player.playerLeft, (player.x, player.y - self.camera))

    def updateplatforms(self, player):
        playerCollider = pygame.Rect(player.x+15, player.y, player.playerRight.get_width()-30,
                                     player.playerRight.get_height())  # Cancel the effect of a long mouth
        # footCollider = pygame.Rect(player.x+10 , player.y+60, player.playerRight.get_width()-20,
        #                              player.playerRight.get_height()-60)
        # Monster colliders
        if self.danger:
            for m in self.monsters:
                if m.kind == 0:  # blackhole
                    monsteRrect = pygame.Rect(m.x, m.y, m.blackhole.get_width() - 25, m.blackhole.get_height() - 20)
                    if monsteRrect.colliderect(playerCollider) and m.kind != 2:
                        player.alive = False
                        # print("die")

                elif m.kind == 1:  # little monster
                    monsteRrect = pygame.Rect(m.x, m.y, m.moveMonster_1.get_width() - 25, m.moveMonster_1.get_height() - 20)
                    if monsteRrect.colliderect(playerCollider) and m.kind != 2:
                        player.alive = False
                        # print("die")

        # Platform and spring colliders
        for p in self.platforms:
            # rect = pygame.Rect(p.x + 10, p.y, p.green.get_width() - 25, p.green.get_height() - 15)
            rect = pygame.Rect(p.x + 10, p.y, p.green.get_width() - 25, 5)
            springRect = pygame.Rect(p.x + p.spring_x + 10, p.y - 20, p.spring.get_width(), p.spring.get_height())
            p.spring_used = False  # spring init

            if rect.colliderect(playerCollider) and player.gravity > 0 and player.y < (p.y - self.camera):
                # jump when landing on green or blue
                if p.kind != 2 and player.alive == True:
                    player.jump = 20
                    player.gravity = 0
                else:
                    # the red broken platform
                    p.broken = True

            # on springs
            if (p.hasSpring == True and springRect.colliderect(playerCollider) and player.gravity > 3.0 and player.y < (
                    p.y - self.camera) and player.alive == True):
                player.jump = 30
                player.gravity = 0
                p.spring_used = True

    # Draw generated platforms and monsters
    def drawplatforms(self):
        # Monsters
        if self.danger:
            for m in self.monsters:
                y = m.y - self.camera
                if y > H:
                    self.monsters.pop(0)
                if m.kind == 1:
                    m.monsterMovement(self.score)

                if m.kind == 0:  # blackhole
                    self.screen.blit(m.blackhole, (m.x, m.y - self.camera))
                elif m.kind == 1:  # moving little monster
                    if m.monsterDirection == 0:
                        self.screen.blit(m.moveMonster_1, (m.x, m.y - self.camera))
                    else:
                        self.screen.blit(m.moveMonster_2, (m.x, m.y - self.camera))
        # Platforms
        for p in self.platforms:
            y = p.y - self.camera
            if y > H and p.broken == False:
                self.generateplatforms(False)
                self.platforms.pop(0)
                self.time = time.time()

            # Blue Platform movement
            if p.kind == 1:
                p.blueMovement(self.score)
            if p.kind == 2:
                if p.broken == True:
                    p.redbreak()
            # Draw platforms
            if p.kind == 0:
                self.screen.blit(p.green, (p.x, p.y - self.camera))
                if p.hasSpring:  # green platform may have springs
                    if not p.spring_used:
                        self.screen.blit(p.spring, (p.x + p.spring_x, p.y - self.camera - 20))
                    else:
                        self.screen.blit(p.spring_1, (p.x + p.spring_x, p.y - self.camera - 20))
            elif p.kind == 1:
                self.screen.blit(p.blue, (p.x, p.y - self.camera))
            elif p.kind == 2:  # red broken platform
                if not p.broken:
                    self.screen.blit(p.red, (p.x, p.y - self.camera))
                else:
                    self.screen.blit(p.red_1, (p.x, p.y - self.camera))

    def generateplatforms(self, initial):
        y = 900  # Generate from bottom of the screen
        start = -100
        if initial == True:  # start the game
            self.startY = -100
            # Fill starting screen with platforms

            while y > -70:
                p = Platform.Platform()
                p.getKind(self.score)  # 0
                p.checkSpring()
                p.y = y
                p.startY = start
                self.platforms.append(p)
                if self.danger:
                    m = monster.Monster()
                    m.getKind(self.score)  # 0
                    m.y = y
                    m.startY = start
                    self.monsters.append(m)

                y -= 30  # Generate every 50 pixels
                start += 30
                self.startY = start
        else:
            # Creates a platform based on current score

            p = Platform.Platform()

            # game difficulty（density）
            difficulty = int(self.score / self.difficultyCoefficient)
            if difficulty > 90:   # up bound
                difficulty = 90
            elif difficulty < 50:  # low bound
                difficulty = 50

            # get new platforms
            p.y = self.platforms[-1].y - difficulty
            self.startY += difficulty
            p.startY = self.startY
            p.getKind(self.score)
            p.checkSpring()
            self.platforms.append(p)

            # get new monsters
            if self.danger:
                m = monster.Monster()
                m.y = self.monsters[-1].y - difficulty
                m.startY = self.startY
                m.getKind(self.score)
                self.monsters.append(m)

    def update(self):
        self.drawplatforms()
        self.screen.blit(self.font.render("Score: " + str(self.score), -1, (0, 0, 0)), (25, 25))
        self.screen.blit(self.font.render("Generation: " + str(self.generation), -1, (0, 0, 0)), (25, 60))

    def loadFtxt(self, file, inputnodes: int, hiddennodes: int, outputnodes: int):
        strr = file.read(-1)
        strr = strr.replace("array", "np.array")
        l = eval(strr)
        cloneBrain = nn.NeuralNetwork(inputnodes, hiddennodes, outputnodes)
        cloneBrain.weights1 = l[0]
        cloneBrain.weights2 = l[1]
        cloneBrain.bias1 = l[2]
        cloneBrain.bias2 = l[3]
        return cloneBrain

    # Run game
    def ga_train(self, load=True):
        clock = pygame.time.Clock()
        TOTAL = 100  # 250 players
        savedDoodler = []
        GA = ga.GeneticAlgorithm()
        if load:
            loadbrain = open("highestbrain.txt", "r")
            brainloaded = self.loadFtxt(loadbrain, Player.INPUT_SIZE, Player.HIDDEN_SIZE, Player.OUTPUT_SIZE)[0]

            doodler = GA.populate(TOTAL, brainloaded)
            loadbrain.close()
        else:
            doodler = GA.populate(TOTAL, None)

        run = True  # start game
        self.generateplatforms(True)
        highestScore = 0
        while run:
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background_image, [0, 0])
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            currentTime = time.time()

            # Clear when stuck
            if currentTime - self.time > 15:
                self.time = time.time()
                for d in doodler:
                    d.fitness = self.score
                    d.fitnessExpo()
                doodler.clear()

            # When all doodlers are dead, create new generation
            if len(doodler) == 0:
                self.camera = 0
                self.time = time.time()
                self.score = 0
                doodler.clear()
                self.platforms.clear()
                self.generateplatforms(True)
                if self.generation > 100 and highestScore < 4000:
                    print("RESET")
                    self.generation = 0
                    doodler = GA.populate(TOTAL, None)

                else:
                    self.generation += 1
                    GA.nextGeneration(TOTAL, savedDoodler)
                    doodler = GA.doodler
                savedDoodler.clear()

            self.update()

            for d in doodler:
                d.fitness = self.score
                d.move(d.think(self.platforms, self.monsters))
                self.drawPlayer(d)
                self.playerUpdate(d)
                self.updateplatforms(d)

                # pygame.draw.rect(self.screen, (255,0,0),(d.x + 50, d.y, 1, 800))
                # pygame.draw.rect(self.screen, (255,0,0), (d.x-600, d.y +50, 600, 1))

                if d.y - self.camera > 800:   # doodle dead
                    # d.fitness = self.score
                    d.fitnessExpo()
                    savedDoodler.append(d)
                    doodler.remove(d)

            if self.score > highestScore:  # update score
                highestScore = self.score
                if len(savedDoodler) != 0:
                    highest = open("highestbrain.txt","w")
                    nbestdoodler = savedDoodler[-3:]
                    highest.write("["+str([nbestdoodler[0].brain.weights1,nbestdoodler[0].brain.weights2,nbestdoodler[0].brain.bias1,nbestdoodler[0].brain.bias2])+','\
                        +str([nbestdoodler[1].brain.weights1,nbestdoodler[1].brain.weights2,nbestdoodler[1].brain.bias1,nbestdoodler[1].brain.bias2])+','\
                        +str([nbestdoodler[2].brain.weights1,nbestdoodler[2].brain.weights2,nbestdoodler[2].brain.bias1,nbestdoodler[2].brain.bias2])+']')
                    highest.close()

            self.screen.blit(self.font.render("Count: " + str(len(doodler)), -1, (0, 0, 0)), (25, 120))
            self.screen.blit(self.font.render("High Score: " + str(highestScore), -1, (0, 0, 0)), (25, 90))

            pygame.display.update()

    def play(self):
        clock = pygame.time.Clock()
        doodler = Player.Player()
        doodler.ai = False

        run = True  # start game
        self.generateplatforms(True)
        highestScore = 0
        while run:
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background_image, [0, 0])
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.update()

            doodler.move()
            self.drawPlayer(doodler)
            self.playerUpdate(doodler)
            self.updateplatforms(doodler)

            if self.score > highestScore:  # update score
                highestScore = self.score

            # self.screen.blit(self.font.render("Count: " + str(len(doodler)), -1, (0, 0, 0)), (25, 120))
            self.screen.blit(self.font.render("High Score: " + str(highestScore), -1, (0, 0, 0)), (25, 90))

            pygame.display.update()

    def qlearning_train(self, maxGeneration = 100, randseed=111):
        # loadbrain = open("latestbrain.txt", "r")
        # brainloaded = self.loadFtxt(loadbrain, 6, 4, 3)[0]
        clock = pygame.time.Clock()
        self.player = Player.Player()
        doodler = self.player
        def getLegalAction(state): return [0,1,2]
        # 0 is right, 1 is left, 2 is middle
        opts = {'actionFn': getLegalAction,'epsilon':0.0,'gamma':1.0,'alpha':0.1}
        qAgent = agent.ApproximateQAgent(extractor='DoodleExtractor',**opts)

        run = True  # start game
        highestScore = 0
        doodleState = DoodleState()
        
        for geneNum in range(maxGeneration):
            Platform.setSeed(randseed)
            if run == False: break
            self.camera = 0
            self.time = time.time()
            self.score = 0
            self.platforms.clear()
            self.generateplatforms(True)
            doodleState.updateState(self.platforms,self.monsters,self.springs,self.player)

            # agent learning
            if geneNum != 0:
                self.player = Player.Player(doodler.brain)
                doodler = self.player

            while True:
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.background_image, [0, 0])
                clock.tick(60)

                if pygame.QUIT in [event.type for event in pygame.event.get()]:
                # Stop training and close the whole game 
                    run = False
                    break
                currentTime = time.time()

                # Clear when stuck
                if currentTime - self.time > 15:
                    self.time = time.time()
                    doodler.alive = False
                    self.generation += 1
                    break

                self.update()

                lastState = DoodleState(doodleState)
                decision = qAgent.computeActionFromQValues(doodleState)
                # print(decision)
                doodler.move(decision)
                # doodler.move()

                self.drawPlayer(doodler)
                self.playerUpdate(doodler)
                self.updateplatforms(doodler)
                doodleState.updateState(self.platforms,self.monsters,self.springs,self.player)
                qAgent.update(lastState,decision,doodleState,-0.1)

                if doodler.y - self.camera > 800:
                    doodler.alive = False
                    self.generation += 1
                    break

                if self.score > highestScore:  # update score
                    highestScore = self.score

                self.screen.blit(self.font.render("High Score: " + str(highestScore), -1, (0, 0, 0)), (25, 90))

                pygame.display.update()

        # Finish traing, wait for space key to end
        self.camera = 0
        self.time = time.time()
        self.score = 0
        self.platforms.clear()
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background_image, [0, 0])
        self.screen.blit(self.font.render("Final socre after "+str(maxGeneration)+" genrations: " + str(highestScore), -1, (0, 0, 0)), (25, 100))
        pygame.display.update()
        while True:
            if pygame.QUIT in [event.type for event in pygame.event.get()]:
                pygame.quit()
                break
            # for event in pygame.event.get():
            #     keys = pygame.key.get_pressed()
            #     if keys[pygame.K_SPACE]:
            #         pygame.quit()





if __name__ == "__main__":
    # Play by player
    # DoodleJump().play()


    # Play by AI
    DoodleJump().ga_train(False)                 # to load a brain, choose True
    #DoodleJump().qlearning_train(maxGeneration=10,randseed = 111)
