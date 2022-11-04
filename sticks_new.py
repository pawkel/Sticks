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