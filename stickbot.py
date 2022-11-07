from stickHuman import StickPlayer
from helpers import (swapHands,fingerTouch,combineActions,decompose)
import numpy as np
import pdb 
class StickBot:
  def __init__(self, botName='Bob', botType=0):
    self.opponent = None
    self.playerID = botName
    self.playerGameID = None
    self.botType = botType
    self.vals = {'l':1,'r':1}

  def nextStates(self, state):
    ''' Calculate next states based on current state
    '''
    sh = swapHands(state, self.playerGameID)
    # print(states)
    ft = fingerTouch(state, self.playerGameID)
    # print(ft) 
    ch = combineActions(state, self.playerGameID)
    # print(ch)
    dc = decompose(state, self.playerGameID)
    # print(dc)
    states = []
    for s in sh+ft+ch+dc:
      if (s not in states) and s!=[]:
        states.append(s)
    return states

  def oneStepAhead_dump(self, states):
    ''' A bot tries to lose as fast as it can? dump...
    '''
    favStates = []
    stateScores = []
    for s in states:
      states2 = self.nextStates(s, -self.playerGameID) ## states that s leads to...
      stateScore = 0
      for s2 in states2:
        if s2[2]==0 or s2[3]==0: ## state 2 and 3 are for opponent's left and right hand
          stateScore += 1
          # break ## if this state leads to a lost, remove it
        elif s2[0]==0 or s2[1]==0: ## state 0 and 1 are for this bot' left and right hand
          stateScore -= 1 ## we just select this winning state!
      # if flag==1:
      #   favStates.append(s)
      stateScores.append(stateScore)
    # try:
    #   idx = np.random.choice(range(len(favStates)),1)[0]
    # except:
    #   print(f'Good game! {self.playerID} resigned!')
    #   return states[np.random.choice(range(len(states)),1)[0]]
    idx = np.argmax(stateScores)
    return favStates[idx]

  def oneStepAhead(self, states, dumb=False):
    favStates = []
    stateScores = []
    for s in states:
      l1,r1, l2,r2 = s
      states2 = self.nextStates((l2,r2,l1,r1)) ## states that s leads to...
      stateScore = 0
      for s2 in states2:
        if s2[2]== s2[3]==0: ## state 2 and 3 are for this bot's left and right hand
          stateScore -= 1
        elif s2[0]==s2[1]==0: ## state 0 and 1 are for opponent's left and right hand
          stateScore += 1
      stateScores.append(stateScore)
    if dumb:
      idx = np.argmin(stateScores)
    else:
      idx = np.argmax(stateScores)
    return favStates[idx]

  def botAI(self, state):
    nStates = self.nextStates(state)
    if self.botType==0: ## randomly select a state
      idx = np.random.choice(range(len(nStates)),1)[0]
      out = nStates[idx]
    elif self.botType==1: ## look one step ahead
      out = self.oneStepAhead(nStates)
    return out

  def addOpponent(self, opponent):
    self.opponent = opponent

  def play(self):
    state = (self.vals['l'], self.vals['r'],
    self.opponent.vals['l'],self.opponent.vals['r'])
    state = self.botAI(state)
    print(self.playerID, ' moved')
    self.vals['l'], self.vals['r'] = state[0],state[1]
    self.opponent.vals['l'],self.opponent.vals['r'] = state[2],state[3] 