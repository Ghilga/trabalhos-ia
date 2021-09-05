import random
import sys
sys.path.append('..')  # i know this is a dirty hack but, you know, time...
import board
import copy
import math

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

STARTING_DEPTH = 1
LIMIT_DEPTH = 10
BOARD_POSITION_WEIGHT = [[120 ,-20 ,20 ,5  ,5  ,20 ,-20 ,120 ],
                         [-20 ,-40 ,-5 ,-5 ,-5 ,-5 ,-40 ,-20 ],
                         [20  ,-5  ,15 ,3  ,3  ,15 ,-5  ,20  ],
                         [5   ,-5  ,3  ,3  ,3  ,3  ,-5  ,5   ],
                         [5   ,-5  ,3  ,3  ,3  ,3  ,-5  ,5   ],
                         [20  ,-5  ,15 ,3  ,3  ,15 ,-5  ,20  ],
                         [-20 ,-40 ,-5 ,-5 ,-5 ,-5 ,-40 ,-20 ],
                         [120 ,-20 ,20 ,5  ,5  ,20 ,-20 ,120 ]]

def make_move(the_board, color):
    """
    Returns an Othello move
    :param the_board: a board.Board object with the current game state
    :param color: a character indicating the color to make the move ('B' or 'W')
    :return: (int, int) tuple with x, y indexes of the move (remember: 0 is the first row/column)
    """
    # o codigo abaixo apenas retorna um movimento aleatorio valido para
    # a primeira jogada com as pretas.
    # Remova-o e coloque a sua implementacao da poda alpha-beta
    
    succ = successors(the_board, color)

    for board in succ:
        print(board)
    print(the_board)

    return random.choice([(2, 3), (4, 5), (5, 4), (3, 2)])


def successors(the_board, color):
    
    possible_boards = []

    for move in the_board.legal_moves(color):
        current_board = copy.deepcopy(the_board)
        current_board.process_move(move,color)
        possible_boards.append(current_board)

    return possible_boards

def stopping_condition(depth):
    return depth > LIMIT_DEPTH
    # --- To be improved ---

def evaluate(state):
    # TODO 
    return ''

def max_value(state, alpha, beta, depth):
    if stopping_condition(depth): return evaluate(state)

    v = -math.inf

    for s in successors(state):
        v = max(v,min_value(s, alpha, beta))
        alpha = max(alpha,v)
        if alpha >= beta:
            break
    
    return v

def min_value(state, alpha, beta, depth):
    if stopping_condition(depth): return evaluate(state)
    
    v = math.inf

    for s in successors(state):
        v = min(v,max_value(s, alpha, beta))
        beta = min(beta,v)
        if beta <= alpha:
            break
    
    return v

def minimax_alpha_beta_decision(state):
    v = max_value(state, -math.inf, math.inf, STARTING_DEPTH)
    return '' # return the action made with the value v

make_move(board.Board(), 'B')