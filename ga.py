import Player
import pygame
import math
import random
import neuralnet as nn
import numpy as np



class GeneticAlgorithm():
    def __init__(self):
        self.best = Player.Player(nn.NeuralNetwork(Player.INPUT_SIZE,Player.HIDDEN_SIZE,Player.OUTPUT_SIZE))
        self.doodler = []
        self.bestFitness = 0

    def populate(self, total, bestBrain):
        
        if (bestBrain is None):
            for i in range(total):
                self.doodler.append(Player.Player(nn.NeuralNetwork(Player.INPUT_SIZE,Player.HIDDEN_SIZE,Player.OUTPUT_SIZE)))  #人物添加
        else:
            historicalbrain = self.loadFtxt("highestbrain.txt",Player.INPUT_SIZE,Player.HIDDEN_SIZE,Player.OUTPUT_SIZE)
            # 考虑要不要让历史最高分的brain有一定权重
            for i in range(total):
                choice = random.randint(0, 3)
                if choice == 0:
                    self.doodler.append(Player.Player(bestBrain.normalchange("weights1")))
                elif choice == 1:
                    self.doodler.append(Player.Player(bestBrain.normalchange("weights2")))
                elif choice == 2:
                    self.doodler.append(Player.Player(bestBrain.normalchange("bias1")))
                elif choice == 3:
                    self.doodler.append(Player.Player(bestBrain.normalchange("bias2")))
                else:
                    pass
                # if choice == 0:
                #     coor = [random.randint(0, 5), random.randint(0, 3)]
                #     self.doodler.append(Player.Player(bestBrain.changeelement("weights1", [6,4], coor, value=None).copy()))
                # elif choice == 1:
                #     coor = [random.randint(0, 3), random.randint(0, 2)]
                #     self.doodler.append(Player.Player(bestBrain.changeelement("weights2", [4,2], coor, value=None).copy()))
                # elif choice == 2:
                #     coor = [random.randint(0, 3)]
                #     self.doodler.append(Player.Player(bestBrain.changeelement("bias1", [4], coor, value=None).copy()))
                # elif choice == 3:
                #     coor = [random.randint(0, 2)]
                #     self.doodler.append(Player.Player(bestBrain.changeelement("bias2", [2], coor, value=None).copy()))
                # else:
                #     pass
                
        return self.doodler

    def nextGeneration(self, total, array):
        self.bestOne(array)

        champion = self.best.clone() 
        self.populate(1, champion.brain)

        champion2 = self.best.clone()                   # Create another clone so it gets mutated in selectOne function
        champion2.fitness = self.bestFitness
        array.append(champion2)
        array.reverse()
        # create random players based on fitness
        for p in range(total -1):
            parent = self.selectOne(array)
            self.populate(1, parent)
        
        array.clear()
        #print("mutated?", self.best.brain.bias1)

    def calculateFitnessSum(self, array):
        # sum fitness
        fitnessSum = math.floor(sum(p.fitness for p in array))

        return fitnessSum

    # Selecting a player with equal probability based on their fitness score 
    def selectOne(self, array):
        fitnessSum = self.calculateFitnessSum(array)
        rand = random.uniform(1,fitnessSum)
        runningSum = 0

        for b in array:
            runningSum += b.fitness
            if(runningSum > rand):
                b.brain.mutate(0.1)
                return b.brain

    # Select the best one of the generation and put into next generation
    def bestOne(self, array):
        max = 0
        currentBest = Player.Player(nn.NeuralNetwork(Player.INPUT_SIZE,Player.HIDDEN_SIZE,Player.OUTPUT_SIZE))

        for b in array:
            if (b.fitness >= max):
                max = b.fitness                     # saves current max fitness
                currentBest = b                     # saves current best player 
        
        # if current best from the generation is better than all-time best
        if (currentBest.fitness >= self.bestFitness):
            #print("BEST")
            self.best = currentBest.clone()                  # clone the current best player 
            self.best.fitness = currentBest.fitness
            self.bestFitness = currentBest.fitness
        
        

        #print("current", currentBest.brain.bias1)
        #print("not mutated", self.best.brain.bias1)
 
    def loadFtxt(self, file, inputnodes: int, hiddennodes: int, outputnodes: int):
        f = open(file)
        strr = f.read(-1)
        strr = strr.replace("array", "np.array")
        # print(strr)
        l = eval(strr)
        cloneBrain = nn.NeuralNetwork(inputnodes, hiddennodes, outputnodes)
        cloneBrain.weights1 = l[0]
        cloneBrain.weights2 = l[1]
        cloneBrain.bias1 = l[2]
        cloneBrain.bias2 = l[3]
        return cloneBrain


