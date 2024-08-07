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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState, 0, 0)[1]

    def minimax(self, gameState, depth, agentIndex):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None

        if agentIndex == 0:
            return self.max_value(gameState, depth)
        else:
            return self.min_value(gameState, depth, agentIndex)

    def max_value(self, gameState, depth):
        v = float('-inf')
        best_action = None
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            value = self.minimax(successor, depth, 1)[0]
            if value > v:
                v = value
                best_action = action
        return v, best_action

    def min_value(self, gameState, depth, agentIndex):
        v = float('inf')
        best_action = None
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            if agentIndex == gameState.getNumAgents() - 1:
                value = self.minimax(successor, depth + 1, 0)[0]
            else:
                value = self.minimax(successor, depth, agentIndex + 1)[0]
            if value < v:
                v = value
                best_action = action
        return v, best_action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.alpha_beta(gameState, 0, 0, float('-inf'), float('inf'))[1]

    def alpha_beta(self, gameState, depth, agentIndex, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None

        if agentIndex == 0:
            return self.max_value(gameState, depth, alpha, beta)
        else:
            return self.min_value(gameState, depth, agentIndex, alpha, beta)

    def max_value(self, gameState, depth, alpha, beta):
        v = float('-inf')
        best_action = None
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            value = self.alpha_beta(successor, depth, 1, alpha, beta)[0]
            if value > v:
                v = value
                best_action = action
            if v > beta:
                return v, best_action
            alpha = max(alpha, v)
        return v, best_action

    def min_value(self, gameState, depth, agentIndex, alpha, beta):
        v = float('inf')
        best_action = None
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            if agentIndex == gameState.getNumAgents() - 1:
                value = self.alpha_beta(successor, depth + 1, 0, alpha, beta)[0]
            else:
                value = self.alpha_beta(successor, depth, agentIndex + 1, alpha, beta)[0]
            if value < v:
                v = value
                best_action = action
            if v < alpha:
                return v, best_action
            beta = min(beta, v)
        return v, best_action


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

        return self.expectimax(gameState, 0, 0)[1]

    def expectimax(self, gameState, depth, agentIndex):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None

        if agentIndex == 0:
            return self.max_value(gameState, depth)
        else:
            return self.exp_value(gameState, depth, agentIndex)

    def max_value(self, gameState, depth):
        v = float('-inf')
        best_action = None
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            value = self.expectimax(successor, depth, 1)[0]
            if value > v:
                v = value
                best_action = action
        return v, best_action

    def exp_value(self, gameState, depth, agentIndex):
        v = 0
        best_action = None
        actions = gameState.getLegalActions(agentIndex)
        p = 1.0 / len(actions)
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            if agentIndex == gameState.getNumAgents() - 1:
                value = self.expectimax(successor, depth + 1, 0)[0]
            else:
                value = self.expectimax(successor, depth, agentIndex + 1)[0]
            v += p * value
        return v, best_action
        

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacman = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghosts = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    score = currentGameState.getScore()
    predict_score = score

    # Distance to closest food
    food_list = food.asList()
    if food_list:
        closest_food_distance = min([manhattanDistance(pacman, food) for food in food_list])
        predict_score += 1.0 / closest_food_distance

    # Distance to ghosts
    ghost_distances = [manhattanDistance(pacman, ghost.getPosition()) for ghost in ghosts]
    for ghost, dist in zip(ghosts, ghost_distances):
        if ghost.scaredTimer > 0:
            predict_score += 10.0 / dist
        else:
            if dist > 0:
                predict_score -= 2.0 / dist

    # Number of remaining food pellets
    predict_score -= 2.0 * len(food_list)

    # Number of remaining power pellets
    predict_score -= 20.0 * len(capsules)

    return predict_score


# Abbreviation
better = betterEvaluationFunction
