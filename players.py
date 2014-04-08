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
def randommc(player,c4,n):
	for action in (col for col in range(6) if c4[6][col]==0):
		c4temp = c4.copy()
		for i in range(n):
			
			

		
