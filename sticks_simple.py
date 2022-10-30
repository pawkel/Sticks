import pygame, numpy as np
player1Left, player1Right = 1,1
player2Left, player2Right = 1,1
clock = pygame.time.Clock()
screen_width = 400
screen_hight = 500
win = pygame.display.set_mode((screen_width,screen_hight))
pygame.display.set_caption("Sticks!")
pygame.init()
def modAll(player1Left, player1Right,player2Left, player2Right):
    player1Right = np.mod(player1Right,5)
    player1Left = np.mod(player1Left,5)
    player2Right = np.mod(player2Right,5)
    player2Left = np.mod(player2Left,5)  
    return player1Left, player1Right, player2Left, player2Right
def actionForPlayerOne(action, player1Left, player1Right, player2Left, player2Right):
    if action == 'll' and player2Left !=0 and player1Left !=0:
        player2Left += player1Left
    elif action == 'lr' and player2Right !=0 and player1Left !=0:
        player2Right += player1Left
    elif action == 'rl' and player2Left !=0 and player1Right !=0:
        player2Left += player1Right
    elif action == 'rr' and player2Right !=0 and player1Right !=0:
        player2Right += player1Right
    elif action == 's' and player1Right !=0 and player1Left !=0:
        player1Right,player1Left = player1Left,player1Right
    elif action == 'cr' and player1Right !=0 and player1Left !=0:
        player1Right = player1Right+player1Left
        player1Left = 0
    elif action == 'cl' and player1Right !=0 and player1Left !=0:
        player1Left = player1Left+player1Right
        player1Right = 0
    else:
        print('Option not found, try again')
        printBoard()
        action = input('ActionP1')
        actionForPlayerOne(action, player1Left, player1Right, player2Left, player2Right)
    return player1Left, player1Right, player2Left, player2Right
def actionForPlayerTwo(action, player1Left, player1Right, player2Left, player2Right):
    if action == 'll' and player1Left !=0 and player2Left !=0:
        player1Left += player2Left
    elif action == 'lr' and player1Right !=0 and player2Left !=0:
        player1Right += player2Left
    elif action == 'rl' and player1Left !=0 and player2Right !=0:
        player1Left += player2Right
    elif action == 'rr' and player1Right !=0 and player2Right !=0:
        player1Right += player2Right
    elif action == 's' and player2Right !=0 and player2Left !=0:
        player2Right,player2Left = player2Left,player2Right
    elif action == 'cr' and player2Right !=0 and player2Left !=0:
        player2Right = player2Right+player2Left
        player2Left = 0
    elif action == 'cl' and player2Right !=0 and player2Left !=0:
        player2Left = player2Left+player2Right
        player1Right = 0
    else:
        print('Option not found, try again')
        printBoard()
        action = input('ActionP2')
        actionForPlayerTwo(action, player1Left, player1Right, player2Left, player2Right)
    return player1Left, player1Right, player2Left, player2Right
def printBoard():
    print('P2:',player2Left,player2Right)
    print('P1:',player1Left,player1Right)
while True:
    pygame.display.update()
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    printBoard()
    if player1Left+player1Right==0:
        print('Player1 Lost :(')
        break
    action = input('ActionP1')
    player1Left, player1Right, player2Left, player2Right = actionForPlayerOne(action, player1Left, player1Right, player2Left, player2Right)
    player1Left, player1Right, player2Left, player2Right = \
        modAll(player1Left, player1Right,player2Left, player2Right)
    printBoard()
    if player2Left+player2Right==0:
        print('Player2 Lost :(')
        break
    action = input('ActionP2')
    player1Left, player1Right, player2Left, player2Right = actionForPlayerTwo(action, player1Left, player1Right, player2Left, player2Right)
    player1Left, player1Right, player2Left, player2Right = \
        modAll(player1Left, player1Right,player2Left, player2Right)
pygame.quit()