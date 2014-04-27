from random import choice
from pylab import *
from util import *

class connect4(object):
    #Creates new game
    def __init__(self, state = None, currPlayer = None, alpha=0.5, w = givenw, ntups = None, verbose = False, shape = (7,6)):
        self.shape = shape 
        self.state = zeros(shape) if state is  None else state
        self.win = None
        self.alpha = alpha
        self.w = w
        self.currPlayer = 1 if currPlayer is None else currPlayer
        self.color = True
        self.ntups = ntups 
        self.verbose = verbose

    def getFeatures(self):
        if self.ntups is not None:
            ks = []
            N = 0
            for tup in self.ntups:
                k = N
                N += 3**len(tup)
                for i,(x,y) in enumerate(tup):
                    s = self.state[x,y]
                    s = 1 if s < 0 else 2 if s > 0 else 0
                    k += s*3**i #3 possible states
                ks.append(k)
            phi = zeros((N,))
            phi[ks] = 1
        else:
            cop = copy(self.state)
            phi = cop.flatten()
        return phi

    def makeNtups(self,n=8,numtups=70):
        #if self.verbose:
        print("Creating %d %d-tuples" % (numtups,n))
        ntups = []
        for i in range(numtups):
            if self.verbose:
                print("Creating tuple %d" %(i+1,))
            x,y = randint(0,self.shape[0]), randint(0,self.shape[1])
            snake = []
            for _ in range(n):
                snake.append((x,y))
                while (x,y) in snake:
                    minx = -1 if x-1 >= 0 else 0 #Inclusive
                    maxx = 2 if x+1 < self.shape[0] else 1 #Exclusive
                    miny = -1 if y-1 >= 0 else 0
                    maxy = 2 if y+1 < self.shape[1] else 1
                    x += randint(minx,maxx)
                    y += randint(miny,maxy)
            ntups.append(snake)
        self.ntups = ntups

    
    def copy(self):
        return connect4(state = copy(self.state),
                        currPlayer = self.currPlayer,
                        shape = self.shape,
                        alpha = self.alpha,
                        w = self.w,
                        ntups = self.ntups,
                        verbose = self.verbose)


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
            
    def learnWFromTd(self, eps = 0.1, alpha = 0.01,
                      numEpisodes = 10000, lamb =0, gamma= 1, useNtups = True):
        if useNtups:
            self.makeNtups()
        n = len(self.getFeatures())
        w = zeros(n,)
        ntups = self.ntups
        e = zeros((n,2))
        for episode in range(numEpisodes):
            trainee = connect4(w = w,ntups=ntups)
            phi = zeros((n,2))
            counter = 0
            while trainee.win is None:
                if self.verbose:
                    print(trainee)
                    print("Learning episode %d of %d" %(episode, numEpisodes))
                counter += 1
                legalMoves = trainee.getLegalMoves()
                if (rand(1)[0] < eps):
                    move = choice(legalMoves)
                else:
                    move = trainee.boardInversionHeuristic(trainee)
                player = trainee.currPlayer
                playerInd = (player+1)//2
                trainee.simulate(move)
                phinew = player*trainee.getFeatures()
                delta = 0 + gamma*logsig(dot(w,phinew)) -logsig((dot(w,phi[:,playerInd])))
                e[:,playerInd] = gamma*lamb*e[:,playerInd]\
                                 +dlogsig(dot(w,phi[:,playerInd]))*transpose(phi[:,playerInd])
                if(counter > 2):
                    w +=  alpha*delta*e[:,playerInd]
                phi[:,playerInd] = phinew
            if trainee.win == 1:
                reward = 1
            elif trainee.win == -1:
                reward = 0
            else:
                reward = 0.5
            
            deltapos = reward - logsig(dot(w,phi[:,0]))
            deltaneg = (1-reward) - logsig(dot(w,phi[:,1]))
            w += alpha*deltapos*e[:,0]
            w += alpha*deltaneg*e[:,1]
            if not self.verbose: 
                print("Learning episode %d of %d" %(episode, numEpisodes),end="\r")
        self.w = w
        return w
                
                  
            

    def boardInversionHeuristic(self,sim):
        features = sim.getFeatures()
        w = self.w
        legalMoves = sim.getLegalMoves()
        if len(legalMoves) == 0:
            return float("-inf") #Don't want to make illegal move.
        phi = zeros((len(w),len(legalMoves)))
        for i,move in enumerate(legalMoves):
            cp = sim.copy()
            cp.simulate(move)
            phi[:,i] = cp.getFeatures()
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
    verbose = bool(int(input("Display board? 1/0: ").split()[-1]))
    dispTrain = bool(int(input("Display Training? 1/0: ").split()[-1]))
    while numPlayers not in range(3):
        numPlayers = int(input("Enter number of players: ").split()[-1])
    if numPlayers < 2:
        posopponents = ["random","MC","MCPlus","Heuristic", "BoardInv","N-tups"]
        opponentChoices = {}
        print("Available opponents:")
        for i,opponent in enumerate(posopponents):
            print("%d. %s" % (i, opponent))
        opponentChoices[-1] = posopponents[int(input("Pick opponent for "+\
                                                     colors[-1] +": ").split()[-1])]
        print(opponentChoices[-1]+" chosen")
        if numPlayers == 0:
            opponentChoices[1] = posopponents[int(input("Pick opponent for "+\
                                                        colors[1] +": ").split()[-1])]
            print(opponentChoices[1]+" chosen")
        
    results = {-1: 0, 0: 0, 1: 0}
    totalRoundsToPlay = 60
    playedRounds = 0
    interactive = False
    startingPlayer = 1
    w = None
    ntups = None
    while play:
        c4 = connect4(currPlayer = startingPlayer,verbose=dispTrain)
        if w is not None:
            c4.w = w
            c4.ntups = ntups
        elif "BoardInv" or "N-tups" in opponentChoices.values():
            print("TD chosen, learning w")
            episodes = int(input("Enter episodes for TD: ").split()[-1])
            print(episodes)
            lamb = float(input("Enter lambda for TD: ").split()[-1])
            print(lamb)
            if "N-tups" in opponentChoices.values():
                w = c4.learnWFromTd(numEpisodes = episodes, lamb = lamb)
                ntups = c4.ntups
            else:
                w = c4.learnWFromTd(numEpisodes = episodes,
                                    lamb = lamb,useNtups = False)
        #c4.w = givenw
        boardInv = lambda : c4.heuristicPlay(heuristicFunc = c4.boardInversionHeuristic)
        opponentActions = {"random": c4.makeRandomMove,
                           "MC": c4.monteCarloPlay,
                           "MCPlus": c4.monteCarloPlayPlus,
                           "Heuristic": c4.heuristicPlay,
                           "BoardInv": boardInv,
                           "N-tups":boardInv}
        win = None
        while win is None:
            if verbose:
                print(c4)
                print("Score: ")
                print(resultsToString(results))
            currPlayer = c4.currPlayer
            if numPlayers == 0:
                if verbose:
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
                    
                

        if verbose:
            print(c4)
        else:
            
            print(resultsToString(results))
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
        
