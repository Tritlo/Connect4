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
for col in range(6):	
    c4Check = c4.copy()
    c4Check.currPlayer*=-1
    state,win = c4Check.simulate(col)
    if win = -c4.currPlayer:
        return col
if __name__=="__main__":
	c4=
