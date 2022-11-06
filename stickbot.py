from stickHuman import StickPlayer
from helpers import (swapHands,fingerTouch,combineActions,decompose)
import numpy as np
import pdb 
class StickBot:
  def __init__(self, botName='Bob'):
    self.opponent = None
    self.playerID = botName
    self.vals = {'l':1,'r':1}

  def candiateMoves(self):
    print(self.vals['l'],self.vals['r'],
    self.opponent.vals['l'],self.opponent.vals['r'])
    states = [swapHands(self.vals['l'],self.vals['r'],
     self.opponent.vals['l'],self.opponent.vals['r'])]
    # print(states)
    ft = fingerTouch(self.vals['l'],self.vals['r'],
    self.opponent.vals['l'],self.opponent.vals['r'])  
    # print(ft) 
    ch = combineActions(self.vals['l'],self.vals['r'],
    self.opponent.vals['l'],self.opponent.vals['r'])
    # print(ch)
    dc = decompose(self.vals['l'],self.vals['r'],
    self.opponent.vals['l'],self.opponent.vals['r'])
    # print(dc)
    for s in ft+ch+dc:
      if (s not in states) and s!=[]:
        states.append(s)
    if [] in states:
      states.remove([])
    # pdb.set_trace()
    return states

  def botAI(self):
    states = self.candiateMoves()
    idx = np.random.choice(range(len(states)),1)[0]
    return states[idx]

  def addOpponent(self, opponent):
    self.opponent = opponent

  def play(self):
    state = self.botAI()
    # pdb.set_trace()
    self.vals['l'], self.vals['r'] = state[0],state[1]
    self.opponent.vals['l'], self.opponent.vals['r'] = state[2],state[3]
    return 


