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
        monsters = state.monsters
        platforms = state.platforms
        vision = player.look(platforms)
        feats = util.Counter()
        feats['inputs[0]'] = vision[1]
        feats['inputs[1]'] = vision[2]
        feats['inputs[2]'] = vision[3]

        xup=player.coordinatesUp - 2*player.xvel -player.x
        xdown = player.coordinatesDown - 2*player.xvel -player.x
        feats['inputs[3]'] = xup%600 if xup%600<abs(xup%600-600) else xup%600-600         # X value of platform above
        feats['inputs[4]'] = xdown%600 if xdown%600<abs(xdown%600-600) else xdown%600-600         # X value of platform below
        feats['inputs[5]'] = monsters[0].x + monsters[0].vel if len(monsters) !=0  else 0
        return feats