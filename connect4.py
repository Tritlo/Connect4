from random import choice
from pylab import *
from util import *


class connect4(object):
    #Creates new game
    def __init__(self, state = None, currPlayer = None,  shape = (7,6),):
        self.shape = shape 
        if state is None:
            self.state = zeros(shape)
        self.win = None
        self.currPlayer = currPlayer if currPlayer else 1
        self.color = True

    def getFeatures(self):
        return self.state[:]
    
    def copy(self):
        return connect4(state = copy(self.state),
                        currPlayer = self.currPlayer,
                        shape = self.shape)

    #Make a legal move
    def makeRandomMove(self):
        legal = lambda x: self.isLegal(x)
        legalMoves = list(filter(legal,range(0,6)))
        move = choice(legalMoves)
        return self.simulate(move)

    def isLegal(self,move):
        t = transpose(self.state)
        fi = find(t[move]==0)
        return len(fi) > 0
        

    # 0 $\leq$ action $\leq$ shape[0]
    # colour = -1 $\wedge$ 1
    def simulate(self,action,colour = None):
        if colour is None:
            colour = self.currPlayer
            self.currPlayer *= -1
            
        t = transpose(self.state)
        indicesWhereEmpty = find(t[action]==0)
        row = argmax(indicesWhereEmpty)
        column = action
        self.state[row][column] = colour
        self.state = transpose(t)
        self.win = self.checkwin(self.state)
        return self.state, self.win
    
    def __str__(self):
        oldOptions = get_printoptions()
        if self.color:
            set_printoptions(linewidth = 79,formatter = {"float":colorPrinter})
            BLUE = '\033[34m'
            ENDC = '\033[0m'
            header = "\n ["
            header += BLUE +" 0"
            header += "   1"
            header += "   2"
            header += "   3"
            header += "   4"
            header += "   5"+ ENDC
            header += " ]\n\n" 
            end = "\n"
        else:
            header = ""
            end = ""
        s = header + str(self.state) + end
        set_printoptions(**oldOptions)
        return  s

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

def colorPrinter(x):
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLACK = '\033[30m'
    BLUE = '\033[34m'
    RED = '\033[31m'
    ENDC = '\033[0m'

    START = "" if x ==0 else RED if x < 0 else BLUE
    ADDSPACE = ' ' if x >= 0 else ""
    if x == 0:
        return "   "
    return START + ADDSPACE+ ("%.0f." % x) + ENDC
        

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
    c4.simulate(4,1)
    c4.simulate(5,1)
    c4.simulate(2,-1)
    c4.simulate(3,-1)
    c4.simulate(3,1)
    print(c4.simulate(3,1))
    print(c4.simulate(3,-1))
    print(c4.simulate(3,-1))
    
    color = True

    def getInput(currPlayer):
        col = int(input("Player " + COLOR + ("%d" % (currPlayer,))\
                        +ENDC+", Enter column: "))
        while col not in range(6):
            print("Incorrect move!")
            col = int(input("Player " + COLOR + ("%d" % (currPlayer,))\
                            +ENDC+", Enter column: "))
        return col
        

    print(c4)
    
    GREEN = '\033[32m'
    BLUE = '\033[34m'
    RED = '\033[31m'
    ENDC = '\033[0m'
    play = True
    numPlayers = -1
    while numPlayers not in range(3):
        numPlayers = int(input("Enter number of players: "))
    while play:
        c4 = connect4()
        win = None
        while win is None:
            print(c4)
            currPlayer = c4.currPlayer
            COLOR = BLUE if currPlayer > 0 else RED
            if numPlayers == 0:
                state, win = c4.makeRandomMove()
            elif numPlayers == 2:
                col = getInput(currPlayer)
                state, win = c4.simulate(col)
            else:
                if currPlayer == 1:
                    col = getInput(currPlayer)
                    state, win = c4.simulate(col)
                else:
                    state, win = c4.makeRandomMove()
                    
                

        print(c4)
        COLOR = BLUE if win > 0 else RED
        if win != 0:
            print("Player " + COLOR + ("%d" % (win,)) +ENDC+" wins!")
        else:
            print(COLOR + "TIE!"+ENDC)
            
        play = input("Play Again, Y/N? ") not in ["N","n","no"]
            
        
    
