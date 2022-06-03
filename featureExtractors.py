# featureExtractors.py
# --------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"Feature extractors for Pacman game states"

from os import stat
import pygame
import DoodleJump
import util

class FeatureExtractor:
    def getFeatures(self, state, action):
        """
          Returns a dict from features to counts
          Usually, the count will just be 1.0 for
          indicator functions.
        """
        util.raiseNotDefined()

class DoodleExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        player = state.player
        lastX, lastY = player.x, player.y
        player.x, player.y = player.getNextPos(action)
        monsters = state.monsters
        platforms = state.platforms
        vision = player.look(platforms)
        coordinatesUp = player.getPlatformAbove(platforms)
        coordinatesDown = player.getPlatformBelow(platforms)

        feats = util.Counter()
        feats['inputs[0]'] = vision[1]
        feats['inputs[1]'] = vision[2]
        feats['inputs[2]'] = vision[3]
        feats["upDown"] = player.upORdown

        xup = coordinatesUp - player.x
        xdown = coordinatesDown - player.x
        feats['inputs[3]'] = abs(xup/600)         # X value of platform above
        feats['inputs[4]'] = abs(xdown/600)         # X value of platform below
        # xmonster = player.getMonsterAbove(monsters)
        # if xmonster != 999:
        #   feats['monsterDist'] = abs((xmonster - player.x)/600)
        player.x, player.y = lastX, lastY
        return feats