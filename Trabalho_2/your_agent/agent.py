import random
import sys
sys.path.append('..')  # i know this is a dirty hack but, you know, time...
import board
import copy
import math
import collections

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

INVERT_COLOR = {'W':'B', 'B':'W'}
CORNER_WEIGHT = 500
POSITION_WEIGHT = 0.5
OPPONENT_COUNT_WEIGHT = 0.25
SURROUNDING_COUNT_WEIGHT = 0.25
STARTING_DEPTH = 1
LIMIT_DEPTH = 4
BOARD_POSITION_WEIGHT = [[120 ,-20 ,20 ,5  ,5  ,20 ,-20 ,120 ],
                         [-20 ,-40 ,-5 ,-5 ,-5 ,-5 ,-40 ,-20 ],
                         [20  ,-5  ,15 ,3  ,3  ,15 ,-5  ,20  ],
                         [5   ,-5  ,3  ,3  ,3  ,3  ,-5  ,5   ],
                         [5   ,-5  ,3  ,3  ,3  ,3  ,-5  ,5   ],
                         [20  ,-5  ,15 ,3  ,3  ,15 ,-5  ,20  ],
                         [-20 ,-40 ,-5 ,-5 ,-5 ,-5 ,-40 ,-20 ],
                         [120 ,-20 ,20 ,5  ,5  ,20 ,-20 ,120 ]]

class GameState:
    
    my_color = ''
    opponent_color = ''

    def __init__(self, game_board, move_played, move_value, player_color):
        # tabuleiro do jogo, com a jogada 'move_played' aplicada. 
        # Usado para geracao de sucessores e para analises na funcao de avaliacao.
        self.game_board = game_board
        # Par ordenado (x,y). Jogada feita. Necessario para o retorno da funcao minimax.
        self.move_played = move_played
        # Inteiro. Valor da jogada feita. Necessario para as comparacoes com alpha e beta no algoritmo
        self.move_value = move_value
        # Cor do jogador que performou a jogada
        self.player_color = player_color
    
    def set_my_color(color):
        GameState.my_color = color
    
    def set_opponent_color(color):
        GameState.opponent_color = color


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

    original_board = GameState(copy.deepcopy(the_board), (-1,-1), -math.inf, color)

    GameState.set_my_color(color)
    GameState.set_opponent_color(INVERT_COLOR[color])

    return minimax_alpha_beta_decision(original_board)


def successors(the_board, color, is_max):

    possible_gameStates = []

    for move in the_board.legal_moves(color):
        current_board = copy.deepcopy(the_board)
        current_board.process_move(move,color)
        current_State = GameState(current_board, move, -math.inf if is_max else math.inf, color)
        possible_gameStates.append(current_State)

    return possible_gameStates

def stopping_condition(depth):
    return depth > LIMIT_DEPTH
    # --- To be improved ---

def can_calculate_surrounding(state):
    x = state[0]
    y = state[1]
    if (x == 0 or x == 7 or y == 7 or y == 0):
        return False
    return True

def get_surrounding_pieces(original_board, state):
    x = state[0]
    y = state[1]
    
    surrounding_pieces = collections.Counter({'W':0, 'B':0})
    surrounding_pieces.update(original_board.tiles[y-1][x-1])
    surrounding_pieces.update(original_board.tiles[y-1][x])
    surrounding_pieces.update(original_board.tiles[y-1][x+1])
    surrounding_pieces.update(original_board.tiles[y][x-1])
    surrounding_pieces.update(original_board.tiles[y][x+1])
    surrounding_pieces.update(original_board.tiles[y+1][x-1])
    surrounding_pieces.update(original_board.tiles[y+1][x])
    surrounding_pieces.update(original_board.tiles[y+1][x+1])

    return surrounding_pieces
    
def get_total_surrounding_pieces(surrounding_pieces):
    return surrounding_pieces['W'] + surrounding_pieces['B']

def get_surrounding_opponent_count(surrounding_pieces, color):
    return surrounding_pieces[INVERT_COLOR[color]]

def get_position_weight(state):
    x = state[0]
    y = state[1]

    return BOARD_POSITION_WEIGHT[y][x]

# TODO NÃO UTILIZADA AINDA
def get_opp_possible_following_plays(board, state, player_color):
    """
    Returns the total number of plays available for the opponent on his next turn, if player_move is performed by the player.
    :param board: a board.Board object
    :param player_move: a (int, int) tuple with x,y coordinates for player's move
    :param player_color: player's color
    :return: int number of plays available for the opponent
    """
    new_board = copy.deepcopy(board)
    new_board.process_move(state, player_color)
    opp_possible_plays = new_board.legal_moves(board.opponent(player_color))
    return -len(opp_possible_plays) 

def is_corner(move):
    if (move in [(0,0), (0,7), (7,0), (7,7)]):
        return True
    return False

def evaluate(game_state):
    if(is_corner(game_state.move_played)):
        return CORNER_WEIGHT

    evaluation_value = (POSITION_WEIGHT*get_position_weight(game_state.move_played))
    #evaluation_value += 2*get_opp_possible_following_plays(game_state.game_board, game_state.move_played, game_state.player_color)
    if(can_calculate_surrounding(game_state.move_played)):
        sorrounding_pieces = get_surrounding_pieces(game_state.game_board, game_state.move_played)
        evaluation_value += OPPONENT_COUNT_WEIGHT*get_surrounding_opponent_count(sorrounding_pieces,game_state.player_color)
        evaluation_value += SURROUNDING_COUNT_WEIGHT*get_total_surrounding_pieces(sorrounding_pieces)
    
    return evaluation_value

def max_value(game_state, alpha, beta, depth):
    if stopping_condition(depth):
        return evaluate(game_state)

    succ = successors(game_state.game_board, GameState.my_color, True)
    if len(succ) == 0:
        if game_state.move_played == (-1,-1):
            return (-1,-1)
        return evaluate(game_state)

    for s in succ:
        game_state.move_value = max(game_state.move_value,min_value(s, alpha, beta, depth+1))
        alpha = max(alpha,game_state.move_value)
        if alpha >= beta:
            break

    if (game_state.move_played == (-1,-1)):
        next_play = succ[0]
        for s in succ:
            if (s.move_value > next_play.move_value):
                next_play = s
        return next_play.move_played
#            if (game_state.move_value == s.move_value):
#                return s.move_played

    return game_state.move_value

def min_value(game_state, alpha, beta, depth):
    if stopping_condition(depth):
        return evaluate(game_state) 

    succ = successors(game_state.game_board, GameState.opponent_color, False)
    if len(succ) == 0:
        return evaluate(game_state)
    
    for s in succ:
        game_state.move_value = min(game_state.move_value,max_value(s, alpha, beta, depth+1))
        beta = min(beta,game_state.move_value)
        if alpha >= beta:
            break
    
    return game_state.move_value

def minimax_alpha_beta_decision(game_state):
    # best_play é o objeto game_state selecionado pelo algoritmo minimax para ser jogado nesse turno.
    best_play = max_value(game_state, -math.inf, math.inf, STARTING_DEPTH)
    return best_play # return the best move
