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
        return  header + str(self.state) + "\n"

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
    if color:
        set_printoptions(linewidth = 79,formatter = {"float":colorPrinter})


    print(c4)
    
    GREEN = '\033[32m'
    BLUE = '\033[34m'
    RED = '\033[31m'
    ENDC = '\033[0m'
    play = True
    while play:
        c4 = connect4()
        currPlayer = -1
        win = None
        while win is None:
            currPlayer *= -1
            print(c4)
            COLOR = BLUE if currPlayer > 0 else RED
            col = int(input("Player " + COLOR + ("%d" % (currPlayer,)) +ENDC+", Enter column: "))
            while col not in range(6):
                print("Incorrect move!")
                col = int(input("Player " + COLOR + ("%d" % (currPlayer,)) +ENDC+", Enter column: "))
            state, win = c4.simulate(col,currPlayer)

        print(c4)
        COLOR = BLUE if win > 0 else RED
        if win != 0:
            print("Player " + COLOR + ("%d" % (win,)) +ENDC+" wins!")
        else:
            print(COLOR + "TIE!"+ENDC)
            
        play = "Y" in input("Play Again, Y/N? ")
            
        
    
