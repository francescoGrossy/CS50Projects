"""
Tic Tac Toe Player
"""
import math
from random import betavariate

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    
    return X if x_count == o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i,j))
    return possible_actions
            


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i,j = action
    if board[i][j] is not EMPTY:
        raise Exception("The position is not empty!")
    new_board = [row[:] for row in board]
    new_board[i][j] = player(board)
    
    return new_board
        


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check rows, columns, and diagonals for a winner
    lines = board + [[board[i][j] for i in range(3)] for j in range(3)] + \
            [[board[i][i] for i in range(3)], [board[i][2 - i] for i in range(3)]]
    for line in lines:
        if all(cell == X for cell in line):
            return X
        elif all(cell == O for cell in line):
            return O
    return None   


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if all(cell != EMPTY for row in board for cell in row):
        return True
    elif winner(board) == X or winner(board) == O:
        return True
    else:
        return False    
        


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = 0
    
    if terminal(board):
       
       if winner(board) == X: result = 1
       elif winner(board) == O: result = -1
           
    return result
        


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)
    if current_player == X:
        return maxvalue(board, -math.inf, +math.inf)[1]
    else:
        return minvalue(board, -math.inf, +math.inf)[1]


def maxvalue(board, alpha, beta):
    if terminal(board):
        return utility(board), None

    v = -math.inf
    best_action = None

    for action in actions(board):
        min_val, _ = minvalue(result(board, action), alpha, beta)
        if min_val > v:
            v = min_val
            best_action = action
        alpha = max(alpha, v)
        if alpha >= beta:
            break

    return v, best_action


def minvalue(board, alpha, beta):
    if terminal(board):
        return utility(board), None

    v = math.inf
    best_action = None

    for action in actions(board):
        max_val, _ = maxvalue(result(board, action), alpha, beta)
        if max_val < v:
            v = max_val
            best_action = action
        beta = min(beta, v)
        if beta <= alpha:
            break

    return v, best_action