import Player
import pygame
import math
import random
import neuralnet as nn



class GeneticAlgorithm():
    def __init__(self):
        self.best = Player.Player(nn.NeuralNetwork(5,4,3))
        self.doodler = []
        self.bestFitness = 0

    def populate(self, total, bestBrain):
        
        if (bestBrain is None):
            for i in range(total):
                self.doodler.append(Player.Player(nn.NeuralNetwork(5,4,3)))  #人物添加
        else:
            for i in range(total):
                self.doodler.append(Player.Player(bestBrain))
                
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
        currentBest = Player.Player(nn.NeuralNetwork(5,4,3))

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
 



