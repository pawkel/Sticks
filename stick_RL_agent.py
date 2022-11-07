#######################################################################
# Copyright (C)                                                       #
# 2016 - 2018 Shangtong Zhang(zhangshangtong.cpp@gmail.com)           #
# 2016 Jan Hakenberg(jan.hakenberg@gmail.com)                         #
# 2016 Tian Jun(tianjun.cpp@gmail.com)                                #
# 2016 Kenta Shimada(hyperkentakun@gmail.com)                         #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################

import numpy as np
import pickle
from helpers import (swapHands,fingerTouch,combineActions,decompose)
import pdb
STICK_SIZE = 2 #
class State:
    def __init__(self):
        # the board is represented by an 1 * 2n array,
        # (P1_STICK1, P1_STICK2, P2_STICK1,P2_STICK2)
        self.data = np.ones(STICK_SIZE*2,dtype='int') ## all stick is one at start
        self.winner = None
        self.hash_val = None
        self.end = None

    # compute the hash value for one state, it's unique
    def hash(self):
        if self.hash_val is None:
            self.hash_val = 0
            for idx, v in enumerate(self.data):
                self.hash_val += int(v*5**idx)
        return self.hash_val

    # check whether a player has won the game, or it's a tie
    def is_end(self):
        if self.end is not None:
            return self.end
        if sum(self.data[STICK_SIZE:]) == 0:
            self.winner = 1
            self.end = True
            return self.end
        if sum(self.data[:STICK_SIZE]) == 0:
            self.winner = -1
            self.end = True
            return self.end
        # game is still going on
        self.end = False
        return self.end

    def next_states(self, player):
        ''' Calculate next states based on current state
        '''
        sw = swapHands(self.data, player)
        ft = fingerTouch(self.data, player)  
        ch = combineActions(self.data, player)
        dc = decompose(self.data, player)
        states = []
        vals = []
        for v in sw+ft+ch+dc:
            if (v not in vals) and v!=[]:
                vals.append(v)
        for s in vals:
            new_state = State()
            new_state.data = s
            states.append(new_state)
        return states

    # print the board
    def print_state(self):
        print('-------------')
        print(f'P2:{self.data[STICK_SIZE:]}')
        print(f'P1:{self.data[:STICK_SIZE]}')
        print('-------------')


def get_all_states_impl(current_state, current_player, all_states):
    new_states = current_state.next_states(current_player)
    for new_state in new_states:
        new_hash = new_state.hash()
        if new_hash not in all_states:
            is_end = new_state.is_end()
            all_states[new_hash] = (new_state, is_end)
            if not is_end:
                get_all_states_impl(new_state, -current_player, all_states)


def get_all_states():
    current_player = 1
    current_state = State()
    all_states = dict()
    all_states[current_state.hash()] = (current_state, current_state.is_end())
    get_all_states_impl(current_state, current_player, all_states)
    return all_states

# all possible stick states
all_states = get_all_states()
class Judger:
    # @player1: the player who will move first, its chessman will be 1
    # @player2: another player with a chessman -1
    def __init__(self, player1, player2):
        self.p1 = player1
        self.p2 = player2
        self.current_player = None
        self.p1_symbol = 1
        self.p2_symbol = -1
        self.p1.set_symbol(self.p1_symbol)
        self.p2.set_symbol(self.p2_symbol)
        self.current_state = State()

    def reset(self):
        self.p1.reset()
        self.p2.reset()

    def alternate(self):
        while True:
            yield self.p1
            yield self.p2

    # @print_state: if True, print each board during the game
    def play(self, print_state=False):
        alternator = self.alternate()
        self.reset()
        current_state = State()
        self.p1.set_state(current_state)
        self.p2.set_state(current_state)
        if print_state:
            current_state.print_state()
        while True:
            player = next(alternator)
            next_state_hash = player.act()
            # next_state_hash = current_state.next_state(i, j, symbol).hash()
            current_state, is_end = all_states[next_state_hash]
            self.p1.set_state(current_state)
            self.p2.set_state(current_state)
            if print_state:
                current_state.print_state()
            if is_end:
                return current_state.winner

# AI player
class Player:
    # @step_size: the step size to update estimations
    # @epsilon: the probability to explore
    def __init__(self, step_size=0.1, epsilon=0.1):
        self.estimations = dict()
        self.step_size = step_size
        self.epsilon = epsilon
        self.states = []
        self.greedy = []
        self.playerGameID = None

    def reset(self):
        self.states = []
        self.greedy = []

    def set_state(self, state):
        self.states.append(state)
        self.greedy.append(True)

    def set_symbol(self, playerGameID):
        self.playerGameID = playerGameID
        for hash_val in all_states:
            state, is_end = all_states[hash_val]
            if is_end:
                if state.winner == self.playerGameID :
                    self.estimations[hash_val] = 1.0
                elif state.winner == 0:
                    # we need to distinguish between a tie and a lose
                    self.estimations[hash_val] = 0.5
                else:
                    self.estimations[hash_val] = 0
            else:
                self.estimations[hash_val] = 0.5

    # update value estimation
    def backup(self):
        states = [state.hash() for state in self.states]

        for i in reversed(range(len(states) - 1)):
            state = states[i]
            td_error = self.greedy[i] * (
                self.estimations[states[i + 1]] - self.estimations[state]
            )
            self.estimations[state] += self.step_size * td_error

    # choose an action based on the state
    def act(self):
        state = self.states[-1]
        new_states = state.next_states(self.playerGameID)
        next_states_hash = [x.hash() for x in new_states]

        if np.random.rand() < self.epsilon:
            action = next_states_hash[np.random.randint(len(next_states_hash))]
            self.greedy[-1] = False
            return action ## return hash_val

        values = []
        for hash_val in next_states_hash:
            try:
                values.append((self.estimations[hash_val], hash_val))
            except:
                print(hash_val)
        # to select one of the actions of equal value at random due to Python's sort is stable
        np.random.shuffle(values)
        values.sort(key=lambda x: x[0], reverse=True)

        action = values[0][1]
        return action

    def save_policy(self):
        with open('policy_%s.bin' % ('first' if self.playerGameID == 1 else 'second'), 'wb') as f:
            pickle.dump(self.estimations, f)

    def load_policy(self):
        with open('policy_%s.bin' % ('first' if self.playerGameID== 1 else 'second'), 'rb') as f:
            self.estimations = pickle.load(f)


# human interface
class HumanPlayer:
    def __init__(self, **kwargs):
        self.state = None
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


    def reset(self):
        pass

    def set_state(self, state):
        self.state = state

    def set_symbol(self, symbol):
        self.symbol = symbol

    def decompose(self, action):
        try:
            leftN  = int(action[1])
            rightN = int(action[2])
        except:
            print(' Second and third characters must be a number between 0 and 4!')
            print(' Try again!')
            self.act()
            return
        returnVal = 0
        if leftN==self.state.data[0] and rightN==self.state.data[1]:
            print(' Bro! That is genius! You just did totally nothing!')
            print(' Try again!')
            self.act()
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
            self.act()
        else:
            self.state.data[0],self.state.data[1] = leftN, rightN
        
    def addOpponent(self, opponent):
        self.opponent = opponent

    def fingerTouch(self, action):
        if action[0]=='l':
            p1_idx = 0
        else:
            p1_idx = 1
        if action[1]=='l':
            p2_idx = 2
        else:
            p2_idx = 3
        if self.state.data[p1_idx]==0:
            print(' You get a zero on this hand, Bro! Try again!')
            self.act()
            return
        elif self.state.data[p2_idx]==0:
            print(" Bro~ That is a dead hand! Do not touch it. I repeat! DON'T!")
            self.act()
            return
        else:
            self.state.data[p2_idx] +=self.state.data[p1_idx]
            self.state.data[p2_idx] = np.mod(self.state.data[p2_idx],5)

    def combineHand(self, action):
        if action[1]=='l':
            self.state.data[0] += self.state.data[1]
            self.state.data[0]= np.mod(self.state.data[0], 5)
            self.state.data[1] = 0
        else:
            self.state.data[1] += np.mod(self.state.data[0],5)
            self.state.data[1]= np.mod(self.state.data[1], 5)
            self.state.data[0] = 0

    def swapHands(self, action):
        if self.state.data[0] !=self.state.data[1]: 
            self.state.data[0], self.state.data[1] = self.state.data[1], self.state.data[0]
        else:
            print(' You have equal number in both hands. Bro! Swapping not allowed!')
            self.act()

    def getStateHash(self):
        new_state = State()
        new_state.data = self.state.data
        return new_state.hash()

    def act(self):
        self.state.print_state()
        action = input(f'Player {self.playerGameID} move: ')
        if action[0]=='d':
            self.decompose(action)
            return self.getStateHash()   
        if action  in self.validActions.keys():
            self.validActions[action](action)
            return self.getStateHash()
        else:
            print(f'  "{action}" is not valid, Bro! Try these:')
            print(f'  {list(self.validActions.keys())}')
            self.play()

def train(epochs, print_every_n=500):
    player1 = Player(epsilon=0.1)
    player2 = Player(epsilon=0.1)
    player1.playerGameID = 1
    player2.playerGameID = -1
    judger = Judger(player1, player2)
    player1_win = 0.0
    player2_win = 0.0
    for i in range(1, epochs + 1):
        winner = judger.play(print_state=False)
        if winner == 1:
            player1_win += 1
        if winner == -1:
            player2_win += 1
        if i % print_every_n == 0:
            print('Epoch %d, player 1 winrate: %.05f, player 2 winrate: %.05f' % (i, player1_win / i, player2_win / i))
        player1.backup()
        player2.backup()
        judger.reset()
    player1.save_policy()
    player2.save_policy()


def compete(turns,print_state):
    player1 = Player(epsilon=0)
    player2 = Player(epsilon=0)
    player1.playerGameID = 1
    player2.playerGameID = -1
    judger = Judger(player1, player2)
    player1.load_policy()
    player2.load_policy()
    player1_win = 0.0
    player2_win = 0.0
    for _ in range(turns):
        winner = judger.play(print_state)
        if winner == 1:
            player1_win += 1
        if winner == -1:
            player2_win += 1
        judger.reset()
    print('%d turns, player 1 win %.02f, player 2 win %.02f' % (turns, player1_win / turns, player2_win / turns))


# The game is a zero sum game. If both players are playing with an optimal strategy, every game will end in a tie.
# So we test whether the AI can guarantee at least a tie if it goes second.
def play(print_state = True):
    while True:
        player1 = HumanPlayer()
        player1.playerGameID = 1
        player2 = Player(epsilon=0)
        player2.playerGameID = -1
        player1.addOpponent(player2)
        judger = Judger(player1, player2)
        player2.load_policy()
        winner = judger.play()

        if winner == player2.playerGameID:
            print("You lose!")
        elif winner == player1.playerGameID:
            print("You win!")
        else:
            print("It is a tie!")


if __name__ == '__main__':
    # train(8_000)
    # compete(int(1e3), print_state=True)
    play(True)
    pass
