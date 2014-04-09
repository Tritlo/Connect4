from random import choice
from pylab import *
from util import *


class connect4(object):
    #Creates new game
    def __init__(self, state = None, currPlayer = None, alpha=0.5, w = givenw,shape = (7,6)):
        self.shape = shape 
        self.state = zeros(shape) if state is  None else state
        self.win = None
        self.alpha = alpha
        self.w = w
        self.currPlayer = 1 if currPlayer is None else currPlayer
        self.color = True

    def getFeatures(self):
        cop = copy(self.state)
        return cop.flatten()
    
    def copy(self):
        return connect4(state = copy(self.state),
                        currPlayer = self.currPlayer,
                        shape = self.shape,
                        alpha = self.alpha,
                        w = self.w)

    #Make a legal move
    def makeRandomMove(self):
        legalMoves = self.getLegalMoves()
        move = choice(legalMoves)
        return self.simulate(move)

    def getLegalMoves(self):
        legal = lambda x: self.isLegal(x)
        return list(filter(legal,range(0,self.shape[1])))
        

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
        
    def rollout(self,move):
        sumReward = 0
        simmove = self.copy()
        state,win = simmove.simulate(move)
        for i in range(5):
            simulation = simmove.copy()
            while win is None:
                state, win = simulation.makeRandomMove()
            sumReward += win
        return sumReward * currPlayer

    def rolloutPlus(self,move):
        sumReward = 0
        player = self.currPlayer
        simmove = self.copy()
        state,win = simmove.simulate(move)
        for i in range(5):
            simulation = simmove.copy()
            while win is None:
                if simulation.currPlayer == player:
                    obvMove = simulation.obviousMove()
                    if  obvMove is not None:
                        state,win = simulation.simulate(obvMove)
                    else:
                        state, win = simulation.makeRandomMove()
                else:
                    state, win = simulation.makeRandomMove()
            sumReward += win
        return sumReward * currPlayer


    def winningMove(self):
        legalMoves = self.getLegalMoves()
        for move in legalMoves:
            simulation = self.copy()
            state, win = simulation.simulate(move)
            if win == self.currPlayer:
                return move
        return None
    
    def blockMove(self):
        legalMoves = self.getLegalMoves()
        for move in legalMoves:
            simulation = self.copy()
            simulation.currPlayer = -1*self.currPlayer
            state,win = simulation.simulate(move)
            if win == -1*self.currPlayer:
                return move
        return None
        

    def obviousMove(self):
        winMove = self.winningMove()
        if winMove is not None:
            return winMove
        blockMove = self.blockMove()
        if blockMove is not None:
            return blockMove
        return None
            

    def boardInversionHeuristic(self,sim):
        features = sim.getFeatures()
        w = self.w
        legalMoves = sim.getLegalMoves()
        phi = zeros((len(w),len(legalMoves)))
        for i,move in enumerate(legalMoves):
            cp = sim.copy()
            cp.simulate(move)
            phi[:,i] = cp.getFeatures()
        #print(phi)
        bestMove= legalMoves[argmax(sim.currPlayer*tansig(dot(w,phi)))]
        return bestMove
            
            
    def monteCarloPlay(self):
        legalMoves = self.getLegalMoves()
        rewards = [self.rollout(move) for move in legalMoves]
        bestMove = legalMoves[argmax(rewards)]
        return self.simulate(bestMove)

    def monteCarloPlayPlus(self):
        obvMove = self.obviousMove()
        if obvMove is not None:
            return self.simulate(obvMove)
        legalMoves = self.getLegalMoves()
        rewards = [self.rolloutPlus(move) for move in legalMoves]
        bestMove = legalMoves[argmax(rewards)]
        return self.simulate(bestMove)

    
    def heuristic(self,sim):
        #Our heuristic here is very similar to
        #The one used by the monte carlo player,
        #Except that we use distance from the win
        #As a metric as well, such that a 
        #win in the next move is much better than a win
        #Two moves later, and a loss in the next move
        #Is worse than a loss two moves later
        #And we average over 7 games.
        #This would cause us to block if possible,
        #and win if possible (how much depends on alpha)
        #but also block in the better way if possible
        #alpha controls how fast the function drops
        alpha = self.alpha
        #alpha = 0.9
        reward = 0
        player = currPlayer
        if sim.win is not None:
            #Large win or punishment for win or loss
            return sim.win*currPlayer*100
        for i in range(5):
            simulation = sim.copy()
            win = None
            count = 0
            while win is None:
                state, win = simulation.makeRandomMove()
                count += 1
            #We exponent alpha to the power of moves.
            #Since it is < 1, it becomes smaller
            #The further away we are.
            reward += 10*win*(alpha**count)
        return reward*currPlayer
        
    
    def heuristicPlay(self, heuristicFunc = None):
        if heuristicFunc is None:
            heuristicFunc = self.heuristic
        legalMoves = self.getLegalMoves()
        simulation = self.copy()
        heuristicVals = []
        for move in legalMoves:
            sim = simulation.copy()
            state,win = sim.simulate(move)
            heuristicVals.append(heuristicFunc(sim))
        
        bestMove = legalMoves[argmax(heuristicVals)]
        return self.simulate(bestMove)
            
            
            
            
        
    def __str__(self):
        oldOptions = get_printoptions()
        if self.color:
            set_printoptions(linewidth = 100,formatter = {"float":colorPrinter})
            BLUE = '\033[34m'
            ENDC = '\033[0m'
            header = "\n ["
            header += BLUE +" 0"
            for i in range(1,self.shape[1]-1):
                header += "   %d" %(i,)
            header += "   " + str(self.shape[1]-1) + ENDC
            header += " ]\n\n" 
            end = "\n"
        else:
            header = ""
            end = ""
        s = header + str(self.state) + end
        set_printoptions(**oldOptions)
        return  s


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

def resultsToString(results):
    st = ""
    for color in [-1,0,1]:
        st += colors[color] + ": "+ str(results[color]) +\
              " "  if color in results else ""
    return st    

def colorPrinter(x):
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLACK = '\033[30m'
    BLUE = '\033[34m'
    RED = '\033[31m'
    ENDC = '\033[0m'

    START = "" if x ==0 else BLUE if x < 0 else RED
    ADDSPACE = ' ' if x >= 0 else ""
    if x == 0:
        return "   "
    return START + ADDSPACE+ ("%.0f." % x) + ENDC
        

if __name__=="__main__":
    
    color = True
    GREEN = '\033[32m'
    BLUE = '\033[34m'
    RED = '\033[31m'
    ENDC = '\033[0m'

    colors = {-1: BLUE+"Blue"+ENDC, 0: "Ties", 1: RED+"Red"+ENDC}
    def getInput(currPlayer):
        col = int(input(colors[currPlayer] + " player, enter column: "))
        while col not in range(7):
            print("Incorrect move!")
            col = int(input(colors[currPlayer] + " player, enter column: "))
        return col
        

    play = True
    numPlayers = -1
    while numPlayers not in range(3):
        numPlayers = int(input("Enter number of players: "))
    if numPlayers < 2:
        posopponents = ["random","MC","MCPlus","Heuristic", "BoardInv"]
        opponentChoices = {}
        print("Available opponents:")
        for i,opponent in enumerate(posopponents):
            print("%d. %s" % (i, opponent))
        opponentChoices[-1] = posopponents[int(input("Pick opponent for "+\
                                                     colors[-1] +": "))]
        if numPlayers == 0:
            opponentChoices[1] = posopponents[int(input("Pick opponent for "+\
                                                        colors[1] +": "))]
        
        
    results = {-1: 0, 0: 0, 1: 0}
    totalRoundsToPlay = 60
    playedRounds = 0
    interactive = False
    startingPlayer = 1
        
    while play:
        c4 = connect4(currPlayer = startingPlayer)
        c4.w = givenw
        boardInv = lambda : c4.heuristicPlay(heuristicFunc = c4.boardInversionHeuristic)
        opponentActions = {"random": c4.makeRandomMove,
                           "MC": c4.monteCarloPlay,
                           "MCPlus": c4.monteCarloPlayPlus,
                           "Heuristic": c4.heuristicPlay,
                           "BoardInv": boardInv}
        win = None
        while win is None:
            print(c4)
            print("Score: ")
            print(resultsToString(results))
            currPlayer = c4.currPlayer
            if numPlayers == 0:
                print("Method: ")
                print(resultsToString(opponentChoices))
                state, win = opponentActions[opponentChoices[currPlayer]]()
            elif numPlayers == 1:
                if currPlayer == 1:
                    col = getInput(currPlayer)
                    state, win = c4.simulate(col)
                else:
                    state, win = opponentActions[opponentChoices[currPlayer]]()
            else:
                col = getInput(currPlayer)
                state, win = c4.simulate(col)
                    
                

        print(c4)
        if win != 0:
            print( colors[win] +" player wins!")
        else:
            print(RED + "Tie!" +ENDC)
        results[win] += 1
        playedRounds += 1
        if interactive:
            play = input("Play Again, Y/N? ") not in ["N","n","no"]
        else:
            play = playedRounds < totalRoundsToPlay
            if playedRounds == totalRoundsToPlay/2:
                print("Swapping players")
                startingPlayer = -1
    print("Final score: ")
    print(resultsToString(results))
    if opponentChoices:
        print("Methods: ")
        print(resultsToString(opponentChoices))
        
