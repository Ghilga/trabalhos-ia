# valueIterationAgents.py
# -----------------------
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


import mdp, util, math

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        newValues = util.Counter()
        for iteration in range(self.iterations):

            for state in self.mdp.getStates():
                if (self.mdp.isTerminal(state) is False):
                    best_action = self.computeActionFromValues(state)
                    newValues[state] = self.computeQValueFromValues(state,best_action)
                '''# usar função para pegar ações possiveis --> actions = self.mdp.getPossibleActions(state)
                best_action = None
                greatest_acc = - math.inf
                best_action_reward = 0
                for action in self.mdp.getPossibleActions(state):
                    # usar função para pegar FUTURAS ações possiveis
                    accumulator = 0
                    reward_acc = 0
                    for nextState, probability in self.mdp.getTransitionStatesAndProbs(state, action):
                        reward_acc += self.mdp.getReward(state, action, nextState) * probability
                        accumulator += currentValues[nextState] * probability
                        
                    if accumulator > greatest_acc:
                        best_action = action
                        greatest_acc = accumulator
                        best_action_reward = reward_acc

                self.values[state] += (best_action_reward) + (discount * greatest_acc)'''
            self.values = newValues.copy()
        
        "*** YOUR CODE HERE ***"


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # obtem uma lista de tuplas (estados, proabilidade de ir para aquele estado) --> nxtStateAndProbsList = self.mdp.getTransitionStatesAndProbs(state, action)
        # fazer o somatorio dos estados*prob --> sum = sum([ getValue(nextState)*Prob for (nextState,Prob) in nxtStateAndProbsList])   
        # return sum
        
        Q_value = sum([(((self.mdp.getReward(state, action, nextState)) + (self.values[nextState] * self.discount)) * probability) for nextState, probability in self.mdp.getTransitionStatesAndProbs(state, action)])
        #print(Q_value)
        #input()
        return Q_value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        # usar função para pegar ações possiveis --> actions = self.mdp.getPossibleActions(state)
        # para cada ação retornada acima calcular os valores de Q --> Q = computeQValueFromValues (...)
        # obtem qual eh o maior Q
        # retorna melhor action

        next_actions = util.Counter()
        for possible_action in self.mdp.getPossibleActions(state):
            next_actions[possible_action] = self.computeQValueFromValues(state, possible_action)
        if((not self.mdp.isTerminal(state)) and len(next_actions) > 0):
            return next_actions.argMax()
        else:
            return None

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)