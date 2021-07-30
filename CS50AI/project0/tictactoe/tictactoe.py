"""
Tic Tac Toe Player
"""
import copy
import math

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
    count = 0
    for i in board:
        count += i.count(EMPTY)

    if count % 2 == 0:
        return O
    else :
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if terminal(board):
        raise NotImplementedError
    elif action not in actions(board):
        raise NotImplementedError
    else:
        new_board = copy.deepcopy(board)
        new_board[action[0]][action[1]]= player(board)
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    Xwin = [X,X,X]
    Owin = [O,O,O]

    winning_positions = [[board[0][0],board[0][1],board[0][2]], 
                    [board[1][0],board[1][1],board[1][2]],
                    [board[2][0],board[2][1],board[2][2]],
                    [board[0][0],board[1][0],board[2][0]],
                    [board[0][1],board[1][1],board[2][1]],
                    [board[0][2],board[1][2],board[2][2]],
                    [board[0][0],board[1][1],board[2][2]],
                    [board[0][2],board[1][1],board[2][0]]]
    
    for win in winning_positions:
        if win==Xwin:
            return X
        elif win == Owin:
            return O
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    for i in board:
        for j in i:
            if j == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    

def max_value(state):
    if terminal(state):
        return utility(state)

    v = -math.inf

    for action in actions(state):
        v = max(v, min_value(result(state, action)))
    return v

def min_value(state):
    if terminal(state):
        return utility(state)

    v = math.inf

    for action in actions(state):
        v = min(v, max_value(result(state, action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if board == initial_state():
        return (1,1)
    
    if player(board) == X:
        v = -math.inf
        optimal_action = None
        for action in actions(board):
            if min_value(result(board, action)) > v:
                v = min_value(result(board, action))
                optimal_action = action
        
    else:
        v = math.inf
        optimal_action = None
        for action in actions(board):
            if max_value(result(board, action)) < v:
                v = max_value(result(board, action))
                optimal_action = action
        
    return optimal_action

    
