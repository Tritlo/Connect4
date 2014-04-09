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
	cumreward = [0]*6
	for action in (col for col in range(6) if c4[6][col]==0):
		reward = range(numRollouts) 
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
			reward[i]=n
		cumreward[action] = sum(reward)
	bestmove=cumreward.index(max(cumreward))
	c4.simulate(bestmove)

def findBlock(c4):
    blockCol = None
    for col in range(6):	
        c4Check = c4.copy()
        c4Check.currPlayer*=-1
        state,win = c4Check.simulate(col)
        if win == -c4.currPlayer:
            blockCol = col
    return blockCol

def findWin(c4):
    winCol = None
    for col in range(6):	
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
        cumreward = [0]*6 
        for action in (col for col in range(6) if c4[6][col]==0):
            reward = range(numRollouts) 
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
                reward[i]=n
            cumreward[action] = sum(reward)
        bestmove=cumreward.index(max(cumreward))
    c4.simulate(bestmove)

if __name__=="__main__":
	c4=connect4()
