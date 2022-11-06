from stickHuman import StickPlayer
from helpers import (swapHands,fingerTouch,combineActions,decompose)
import numpy as np
import pdb 
class StickBot:
  def __init__(self, botName='Bob'):
    self.opponent = None
    self.playerID = botName
    self.vals = {'l':1,'r':1}

  def nextStates(self, state):
    ''' Calculate next states based on current state
    '''
    l1,r1,l2,r2  = state
    states = [swapHands(l1,r1,l2,r2)]
    # print(states)
    ft = fingerTouch(l1,r1,l2,r2)  
    # print(ft) 
    ch = combineActions(l1,r1,l2,r2)
    # print(ch)
    dc = decompose(l1,r1,l2,r2)
    # print(dc)
    for s in ft+ch+dc:
      if (s not in states) and s!=[]:
        states.append(s)
    if [] in states:
      states.remove([])
    return states

  def oneStepAhead(self, states):
    favStates = []
    for s in states:
      l1, r1, l2,r2 = s
      states2 = self.nextStates((l2,r2, l1,r1)) ## states that s leads to...
      flag = 1
      for s2 in states2:
        if s2[2]==s2[3]==0:
          flag = 0
          break ## if this state leads to a lost, remove it
      if flag==1:
        favStates.append(s)
    try:
      idx = np.random.choice(range(len(favStates)),1)[0]
    except:
      print(f'Good game! {self.playerID} resigned!')
      return states[np.random.choice(range(len(states)),1)[0]]
    return favStates[idx]

  def botAI(self, option=0):
    state = (self.vals['l'], self.vals['r'],
    self.opponent.vals['l'],self.opponent.vals['r'])
    nStates = self.nextStates(state)
    if option==0: ## randomly select a state
      idx = np.random.choice(range(len(nStates)),1)[0]
      out = nStates[idx]
    elif option==1: ## look one step ahead
      out = self.oneStepAhead(nStates)
    return out

  def addOpponent(self, opponent):
    self.opponent = opponent

  def play(self):
    state = self.botAI(1)
    print(self.playerID, ' moved')
    self.vals['l'], self.vals['r'] = state[0],state[1]
    self.opponent.vals['l'],self.opponent.vals['r'] = state[2],state[3] 