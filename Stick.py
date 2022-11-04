import numpy as np

class StickPlayer:
  def __init__(self, id=0) -> None:
    self.playerID = id
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
    if leftN==rightN==self.vals['r']==self.vals['l']:
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
    else:
      self.opponent.vals[action[1]] +=self.vals[action[0]]
      self.opponent.vals[action[1]] = np.mod(self.opponent.vals[action[1]],5)

  def combineHand(self, action):
    if action[1]=='l':
      self.vals['l'] += np.mod(self.vals['r'],5)
      self.vals['r'] = 0
    else:
      self.vals['r'] += np.mod(self.vals['l'],5)
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



class StickGameBoard:
  def __init__(self) -> None: 
    self.players = [StickPlayer(1), StickPlayer(2)]
    self.players[0].addOpponent(self.players[1])
    self.players[1].addOpponent(self.players[0])
    self.turnNum = 0
    self.status = 1
    self.gameManul()

  def gameManul(self):
    print('Welcome to the fun sticks game!')
    print('You and your opponent both start with two sticks. One in each hand')
    print("Your goal is to increase your opponent's sticks to exactly FIVE at either hand")
    print('You can do these actions:')
    print(list(self.players[0].validActions.keys())+['dXY'])

  def NextMove(self):
    currentPlayerID = np.mod(self.turnNum,2)
    nextPlayerID = np.mod(self.turnNum+1,2)
    self.players[currentPlayerID].play()
    self.players[nextPlayerID]= self.players[currentPlayerID].opponent
    self.checkGameStatus()
    self.turnNum +=1

  def checkGameStatus(self):
    ''' check if any player has zeros on both hands
    if so, gameover!
    '''
    for p in self.players:
      if sum(p.vals.values())==0: ## calcuate total values for this player
        print(f'Player {p.playerID} lost!')
        self.status = -1

  def printBoard(self):
    gameScoreInfo = ''
    for i in range(2):
      gameScoreInfo  +=f"P{i+1}-> {list(self.players[i].vals.values())}\n"
    print(gameScoreInfo)

  def rematch(self):
    ''' rematch. Initiat all variables
    '''
    for p in self.players:
      p.vals['r'], p.vals['l'] = 1, 1
    self.turnNum = 0
    self.status = 1

if __name__=='__main__':
  from Stick import  StickGameBoard
  game = StickGameBoard()
  while game.status !=-1: ## game end if status is -1
      game.NextMove()
      game.printBoard()
      if game.status ==-1:
        rmt=input('Game finished. Rematch?')
        if rmt in ['y','Y']:
          game.rematch()
        else:
          print('too soon~~See you next time! Bye!')