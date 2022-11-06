import numpy as np
from enum import Enum
from stickbot import StickBot
from stickHuman import StickPlayer
import datetime
import pdb
class StickGameType(Enum):
  HumanVsHuman = 1
  HumanVsBot = 2
  BotVsBot = 3

class StickGameBoard:
  def __init__(self, gameType = StickGameType.HumanVsHuman) -> None: 
    if gameType==None:
      gameType = int(input('Choose a game type:1. Human vs Human;2. Human vs Bot. 3. Bot vs Bot:'))

    if gameType == StickGameType.HumanVsHuman.value:
      self.players = [StickPlayer(1), StickPlayer(2)]
    elif gameType == StickGameType.HumanVsBot.value:
      self.players = [StickPlayer(1), StickBot()]
    elif gameType == StickGameType.BotVsBot.value:
      self.players = [StickBot(botName='Nobody'), StickBot(botName='Owen')]
    
    ## add opponent's reference
    self.players[0].addOpponent(self.players[1])
    self.players[1].addOpponent(self.players[0])
    ## get PlayerGameID (0 or 1) for check score and other status
    self.players[0].playerGameID = 0
    self.players[1].playerGameID = 1

    self.turnNum = 0
    self.status = 1
    if gameType != StickGameType.BotVsBot:
      self.gameManul()
    self.randomSeed = np.random.seed(datetime.datetime.now().microsecond)

  def gameManul(self):
    print(datetime.datetime.now())
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
    for i in [1,0]:
      gameScoreInfo  +=f"Player {self.players[i].playerID} -> {list(self.players[i].vals.values())}\n"
    print(gameScoreInfo)

  def rematch(self):
    ''' rematch. Initiat all variables
    '''
    for p in self.players:
      p.vals['r'], p.vals['l'] = 1, 1
    self.turnNum = 0
    self.status = 1
    self.randomSeed = np.random.seed(datetime.datetime.now().microsecond)

if __name__=='__main__':
  from Stick import  StickGameBoard
  game = StickGameBoard(gameType)
  while game.status !=-1: ## game end if status is -1
      game.NextMove()
      game.printBoard()
      if game.status ==-1:
        rmt=input('Game finished. Rematch?')
        if rmt in ['y','Y']:
          game.rematch()
        else:
          print('too soon~~See you next time! Bye!')