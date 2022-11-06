import numpy as np
class StickPlayer:
  def __init__(self, id=0) -> None:
    self.playerID = id ## player's name
    self.playerGameID = None  ## player's inGame id
    self.opponent = None
    self.vals = {'l':1,'r':1}
    self.validActions = {
      'll':  self.fingerTouch,
      'rr':  self.fingerTouch,
      'lr':  self.fingerTouch,
      'rl':  self.fingerTouch,
      's':   self.swapHands,
      'cl':  self.combineHand,
      'cr':  self.combineHand
    }

  def decompose(self, action):
    try:
      leftN  = int(action[1])
      rightN = int(action[2])
    except:
      print(' Second and third characters must be a number between 0 and 4!')
      print(' Try again!')
      self.play()
      return
    returnVal = 0
    if leftN==self.vals['l'] and rightN==self.vals['r']:
      print(' Bro! That is genius! You just did totally nothing!')
      print(' Try again!')
      self.play()
      return     

    if leftN+rightN != sum(self.vals.values()):
      print(' Numbers do not add up! Learn some math, Bro!')
      returnVal += 1
    if leftN>5 or leftN<0 or rightN>5 or rightN<0:
      print(' Values not allowed, must between(0, 4)')
      returnVal += 1
    if returnVal != 0:
      if returnVal > 1:
        print(f' Bro~~ You made {returnVal} mistakes! So insulting!')
      print(' Try again!')
      self.play()
    else:
      self.vals['l'],self.vals['r'] = leftN, rightN
    
  def addOpponent(self, opponent):
    self.opponent = opponent

  def fingerTouch(self, action):
    if self.vals[action[0]]==0:
      print(' You get a zero on this hand, Bro! Try again!')
      self.play()
      return
    elif self.opponent.vals[action[1]]==0:
      print(" Bro~ That is a dead hand! Do not touch it. I repeat! DON'T!")
      self.play()
      return
    else:
      self.opponent.vals[action[1]] +=self.vals[action[0]]
      self.opponent.vals[action[1]] = np.mod(self.opponent.vals[action[1]],5)

  def combineHand(self, action):
    if action[1]=='l':
      self.vals['l'] += self.vals['r']
      self.vals['l']= np.mod(self.vals['l'], 5)
      self.vals['r'] = 0
    else:
      self.vals['r'] += np.mod(self.vals['l'],5)
      self.vals['r']= np.mod(self.vals['r'], 5)
      self.vals['l'] = 0

  def swapHands(self, action):
    if self.vals['l'] !=self.vals['r']: 
      self.vals['l'], self.vals['r'] = self.vals['r'], self.vals['l']
    else:
      print(' You have equal number in both hands. Bro! Swapping not allowed!')
      self.play()

  def play(self):
    action = input(f'Player {self.playerID} move: ')
    if action[0]=='d':
      self.decompose(action)
      return 
    if action  in self.validActions.keys():
      self.validActions[action](action)
    else:
      print(f'  "{action}" is not valid, Bro! Try these:')
      print(f'  {list(self.validActions.keys())}')
      self.play()