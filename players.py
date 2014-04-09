from pylab import *
from util import *
from connect4 import *

#player =1 or -1, c4 is a connect4 object
"""def randommove(player,c4):
    action = random.randint(0,5)
    # check if we have room in the chosen column
    while c4[6][action]!=0:
        action=random.randint(0,5)
    c4.simulate(action,player)
"""
def randommc(c4,numRollouts):
    cumreward = [-8]*7
    for action in (col for col in range(6) if c4.isLegal(col)):
        reward = [0]*numRollouts 
        for i in range(numRollouts):
            c4temp = c4.copy()
            win = None
            state,win =c4temp.simulate(action)
            while win is None:
                state,win = c4temp.makeRandomMove()
            if win == 0:
                r = 0.5
            else:
                r = win*c4.currPlayer
            reward[i] = r
        cumreward[action] = sum(reward)
    bestmove = cumreward.index(max(cumreward))
    state, win = c4.simulate(bestmove)
    return state, win

def findBlock(c4):
    blockCol = None
    for col in (col for col in range(6) if c4.isLegal(col)):
        c4Check = c4.copy()
        c4Check.currPlayer*=-1
        state,win = c4Check.simulate(col)
        if win == -c4.currPlayer:
            blockCol = col
    return blockCol

def findWin(c4):
    winCol = None
    for col in (col for col in range(6) if c4.isLegal(col)):
        c4Check = c4.copy()
        state,win = c4Check.simulate(col)
        if win == c4.currPlayer:
            winCol=col
    return winCol


def smartermc(c4,numRollouts):
    winningMove = findWin(c4)
    blockMove = findBlock(c4)
    if winningMove != None:
        bestmove = winningMove
    elif blockMove != None:
        bestmove = blockMove
    else:
        cumreward = [-8]*7 
        for action in (col for col in range(6) if c4.isLegal(col)):
            reward = [0]*numRollouts 
            for i in range(numRollouts):
                c4temp = c4.copy()
                win = None
                state,win =c4temp.simulate(action)
                while win is None:
                    winningMove = findWin(c4)
                    blockMove = findBlock(c4)
                    if winningMove != None:
                        state, win = c4temp.simulate(winningMove)
                    elif blockMove != None:
                        state, win = c4temp.simulate(blockMove)
                    else:
                        state,win = c4temp.makeRandomMove()
                if win == 0:
                    r = 0.5
                else:
                    r = win*c4.currPlayer
                reward[i]=r
            cumreward[action] = sum(reward)
        bestmove=cumreward.index(max(cumreward))
    state, win = c4.simulate(bestmove)
    return state, win

if __name__=="__main__":
    c4=connect4()
    play = True
    results = {-1: 0, 0: 0, 1: 0}
    autoplayRounds = 2
    while play:
        c4 = connect4()
        win = None
        while win is None:
            if c4.currPlayer ==1:
                state, win = randommc(c4,5)
            else:
                state,win = smartermc(c4,5)
        print(c4)
        COLOR = "BLUE" if win > 0 else "RED"
        if win != 0:
            print("Player " + COLOR + ("%d" % (win,))+"wins!")
        else:
            print(COLOR + "TIE!")
        results[win] += 1
        autoplayRounds -= 1
        play = autoplayRounds > 0
    print(results)
