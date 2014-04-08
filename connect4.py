from pylab import *
from util import *


class connect4(object):
    #Creates new game
    def __init__(self, shape = (7,6)):
        self.shape = shape 
        self.state = zeros(shape)
        self.win = None

    def getFeatures(self):
        return self.state[:]

    # 0 $\leq$ action $\leq$ shape[0]
    # colour = -1 $\wedge$ 1
    def simulate(self,action,colour):
        t = transpose(self.state)
        row = argmax(find(transpose(self.state)[action]==0))
        column = action
        self.state[row][column] = colour
        self.state = transpose(t)
        self.win = self.checkwin(self.state)
        return self.state, self.win
    
    def __str__(self):
        return str(self.state)

    def reward(self, colour, row, column):
        return win

    # 0 is draw, 1,-1 is win for that colour, None is game not over
    def checkwin(self, state):
        s = state.flatten()
        for winpos in winningLocations:
            posSum = sum(s[winpos])
            if abs(posSum) == 4:
                return sign(posSum)

        if all(state,1)[0]:
            return 0
        return None

        

if __name__=="__main__":
    c4 = connect4()
    c4.simulate(0,1)
    c4.simulate(0,-1)
    c4.simulate(1,1)
    c4.simulate(1,1)
    c4.simulate(1,-1)
    c4.simulate(2,1)
    c4.simulate(2,1)
    c4.simulate(2,1)
    c4.simulate(2,-1)
    c4.simulate(3,-1)
    c4.simulate(3,1)
    print(c4.simulate(3,1))
    print(c4.simulate(3,-1))
    print(c4.simulate(3,-1))
    print(c4)
    
    play = False
    if play:
        c4 = connect4()
        currPlayer = 1
        print(c4)
        col = int(input("Player %d, Enter column: " % (currPlayer,)))
        state, win = c4.simulate(col,currPlayer)
        while win is None:
            currPlayer *= -1
            print(c4)
            col = int(input("Player %d, Enter column: " % (currPlayer,)))
            state, win = c4.simulate(col,currPlayer)

        print(c4)
        print("Player %d wins!" % (win,))
        
    
