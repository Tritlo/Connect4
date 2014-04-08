from pylab import *

from util import *

class connect4:
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
        self.win = self.checkwin(colour,row,column)
        return self.state, self.win

    def reward(self, colour, row, column):
        return win

    # 0 is draw, 1,-1 is win for that colour, None is game not over
    def checkwin(self, colour, row, column):
        s = self.state
        minrow = row - 4 if row - 4 > 0 else 0
        maxrow = row + 4 if row + 4 < self.shape[0] else self.shape[0]
        mincol = column - 4 if column - 4 > 0 else 0
        maxcol = column + 4 if column + 4 < self.shape[1] else self.shape[1]
        
        #Horiz
        for j in range(mincol, maxcol-3):
            if all(s[row][j:j+4] == colour):
                return colour, "horiz"
                    
        #Verti
        if row + 4 < self.shape[0]:
            if all(transpose(s[row:row+4][:])[column] == colour):
                return colour

        #Check diagonals
        sm = s[minrow:minrow+6,mincol:mincol+6]
        smf = fliplr(sm)
        for i in range(3):
            dsms = [diagonal(sm,i) ,diagonal(sm,-i) ,diagonal(smf,i) ,diagonal(smf,-i)]
            for dsm in dsms:
                if colour in dsm and len(find(dsm == colour)) >= 4:
                    for i in range(0,len(dsm)-3):
                        if all(dsm[i:i+4] == colour):
                            return colour
                
                
        #Draw
        if all(self.state,1)[0]:
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
    c4.simulate(3,1)
    c4.simulate(3,1)
    print c4.simulate(3,-1)
    print c4.state
    
