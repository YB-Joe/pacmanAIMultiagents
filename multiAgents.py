# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) 

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        evalue = 0
        if currentGameState.getFood()[successorGameState.getPacmanPosition()[0]][successorGameState.getPacmanPosition()[1]]: #check the pacman position == current state food position on the next state
          evalue += 200 # give the score
        score = 999999 #for the distance declare the infinite number
        
        for f in newFood.asList(): 
          food2distance = manhattanDistance(newPos,f) #use manhattanDistance to calculate the distance between food and pacman position
          score = min([999999, food2distance]) # for the min value
        for g in newGhostStates: # for the ghost position 
          g2distance = manhattanDistance(g.getPosition(), newPos) # use manhattanDistance to calculate the distance beteen the ghost and pacman.
               
        if min([g2distance]) > 2: #check the distance between pacman and ghost is less tahn 2
          evalue += 400
        else:
          evalue -= 400
        return evalue + (float(10)/score)  + (min([g2distance])/40) + currentGameState.getScore() #return the score and distance
        

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def maxfunction(gamestate, depth, agentIndex): 
          if depth == self.depth:#check current depth 
            return self.evaluationFunction(gamestate)
          elif gamestate.isWin() ==1 or gamestate.isLose() == 1: #check the game is win or lose
            return self.evaluationFunction(gamestate)
          elif gamestate.isWin() !=1 or gamestate.isLose() != 1:  #if not
            score = -999999
            for a in gamestate.getLegalActions():
              score =  max(score, minfunction(gamestate.generateSuccessor(0,a), depth, 1))
            return score

        def minfunction(gamestate, depth, agentIndex): #minfunction 
          if depth == self.depth: 
            return self.evaluationFunction(gamestate)
          elif gamestate.isWin() ==1 or gamestate.isLose() ==1:#check the game is win or lose
            return self.evaluationFunction(gamestate)
          elif gamestate.isWin() !=1 or gamestate.isLose() != 1:#if not
            score = 999999
            for a in gamestate.getLegalActions(agentIndex):
              if agentIndex+1 != gamestate.getNumAgents():
                score = min(score, minfunction(gamestate.generateSuccessor(agentIndex, a), depth,agentIndex +1))
              elif agentIndex+1 == gamestate.getNumAgents():
                score = min(score, maxfunction(gamestate.generateSuccessor(agentIndex, a), depth + 1, 0))
            return score

        var = gameState.getLegalActions()
        score = -9999999
        for a in gameState.getLegalActions():
        
          if score <= minfunction(gameState.generateSuccessor(0, a), 0, 1):#compare the minfuntion and score
            score = minfunction(gameState.generateSuccessor(0, a), 0, 1)
            var = a
        return var
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        def prunning(gamestate,depth ,agentIndex, A, B): #prunning function
            if agentIndex > 0:  #if agent index is larger than zeri
                return minfunction(gamestate,depth,agentIndex, A, B) #just return the minfuntion
            if agentIndex <= 0:  #if not, just return the max funtion
                return maxfunction(gamestate,depth, agentIndex, A, B)
        def maxfunction(gamestate,depth,agentIndex, A, B):  # max function
            if depth == self.depth: #check the depth
              return self.evaluationFunction(gamestate)
            elif gamestate.isWin() ==1 or gamestate.isLose() ==1:
              return self.evaluationFunction(gamestate)
            score = -9999999
            for a in gamestate.getLegalActions(agentIndex):
                p_val = prunning(gamestate.generateSuccessor(agentIndex, a),depth,1, A, B)
                score = max(score, p_val)
                if score > B:
                    return score
                A = max(A, score)
            return score

        def minfunction(gamestate,depth,agentIndex, A, B): #minfunction
            if depth == self.depth: 
              return self.evaluationFunction(gamestate)
            elif gamestate.isWin() ==1 or gamestate.isLose() ==1:
              return self.evaluationFunction(gamestate)  
            score = 99999999
            for a in gamestate.getLegalActions(agentIndex):
              if agentIndex+1 != gamestate.getNumAgents():
                p_val = prunning(gamestate.generateSuccessor(agentIndex, a),depth, agentIndex+1, A, B) #p_value == prunnging
                score = min(p_val, score)
                if score < A: #if score is less than the value of alpha
                    return score
                B = min(B, score)
              elif agentIndex+1 == gamestate.getNumAgents():
                p_val = prunning(gamestate.generateSuccessor(agentIndex, a),depth+1, 0, A, B)#p_value == prunning
                score = min(p_val, score)
                if score < A:#if score is less than the value of alpha
                    return score
                B = min(B, score)
            return score
        
        var = gameState.getLegalActions()
        p_val = -999999
        A = -9999999 #alpha
        B = 999999 #Beta
        for a in gameState.getLegalActions():
            if prunning(gameState.generateSuccessor(0, a),0 ,1,A, B) > p_val:
                p_val = prunning(gameState.generateSuccessor(0, a),0 ,1,A, B)
                var = a
            if p_val > B:
              return p_val
            A = max(A, p_val)
        return var
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maxfunction(gamestate, depth, agentIndex):
          if depth == self.depth:#check the current depth
            return self.evaluationFunction(gamestate)
          elif gamestate.isWin() ==1 or gamestate.isLose() == 1:
            return self.evaluationFunction(gamestate)
          elif gamestate.isWin() !=1 or gamestate.isLose() != 1:  
            score = -999999
            for a in gamestate.getLegalActions():
              score =  max(score, expectimax(gamestate.generateSuccessor(0,a), depth, 1))#amx function
            return score
        def expectimax(gamestate, depth, agentIndex): #expectimax function
          if depth == self.depth or gamestate.isWin() or gamestate.isLose():
            return self.evaluationFunction(gamestate)
          p_val = 0
          if agentIndex+1 != gamestate.getNumAgents():
            for a in gamestate.getLegalActions(agentIndex):
              p_val += expectimax(gamestate.generateSuccessor(agentIndex, a), depth, agentIndex+1)/len(gamestate.getLegalActions(agentIndex))
          elif agentIndex+1 == gamestate.getNumAgents():
            for a in gamestate.getLegalActions(agentIndex):
              p_val += maxfunction(gamestate.generateSuccessor(agentIndex, a), depth + 1, 0)/len(gamestate.getLegalActions(agentIndex))
          return p_val
        var = gameState.getLegalActions()
        p_val = -999999
        for a in gameState.getLegalActions():
          if expectimax(gameState.generateSuccessor(0, a), 0, 1) > p_val:
            p_val = expectimax(gameState.generateSuccessor(0, a), 0, 1)
            var = a
        return var
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: evlauation value based on evaluation function above but some variables and weights are updated.
      current score, distance between food and pacman position, distance between the ghost and pacman position. 
      return the evaluation value and score, ghost distance, and current score
    """
    
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    evalue = 0
    if currentGameState.getFood()[currentGameState.getPacmanPosition()[0]][currentGameState.getPacmanPosition()[1]]: #check the pacman position == current state food position on the next state
      evalue += 1500 # give the score
    score = 999999 #for the distance declare the infinite number
        
    for f in newFood.asList(): 
      food2distance = manhattanDistance(newPos,f) #use manhattanDistance to calculate the distance between food and pacman position
      score = min([999999, food2distance]) # for the min value
    for g in newGhostStates: # for the ghost position 
      g2distance = manhattanDistance(g.getPosition(), newPos) # use manhattanDistance to calculate the distance beteen the ghost and pacman.
               
    if min([g2distance]) > 10: #check the distance between pacman and ghost is less tahn 2
      evalue += 400
    else:
      evalue -= 40
    return evalue + (1.0/score)  + -2*(max([g2distance])) + currentGameState.getScore() #return the score and distance
    util.raiseNotDefined()
    

# Abbreviation
better = betterEvaluationFunction

