# use math library if needed
import math

def get_child_boards(player, board):
    """
    Generate a list of succesor boards obtained by placing a disc 
    at the given board for a given player
   
    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the player that will place a disc on the board
    board: the current board instance

    Returns
    -------
    a list of (col, new_board) tuples,
    where col is the column in which a new disc is placed (left column has a 0 index), 
    and new_board is the resulting board instance
    """
    
    res = []
    for c in range(board.cols):
        if board.placeable(c):
            tmp_board = board.clone()
            tmp_board.place(player, c)
            res.append((c, tmp_board))
    return res


def evaluate(player, board):
    """
    This is a function to evaluate the advantage of the specific player at the
    given game board.

    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the specific player
    board: the board instance

    Returns
    -------
    score: float
        a scalar to evaluate the advantage of the specific player at the given
        game board
    """
    adversary = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
    # Initialize the value of scores
    # [s0, s1, s2, s3, --s4--]
    # s0 for the case where all slots are empty in a 4-slot segment
    # s1 for the case where the player occupies one slot in a 4-slot line, the rest are empty
    # s2 for two slots occupied
    # s3 for three
    # s4 for four
    score = [0]*5
    adv_score = [0]*5

    # Initialize the weights
    # [w0, w1, w2, w3, --w4--]
    # w0 for s0, w1 for s1, w2 for s2, w3 for s3
    # w4 for s4
    weights = [0, 1, 4, 16, 1000]

    # Obtain all 4-slot segments on the board
    seg = []
    invalid_slot = -1
    left_revolved = [
        [invalid_slot]*r + board.row(r) + \
        [invalid_slot]*(board.rows-1-r) for r in range(board.rows)
    ]
    right_revolved = [
        [invalid_slot]*(board.rows-1-r) + board.row(r) + \
        [invalid_slot]*r for r in range(board.rows)
    ]
    for r in range(board.rows):
        # row
        row = board.row(r) 
        for c in range(board.cols-3):
            seg.append(row[c:c+4])
    for c in range(board.cols):
        # col
        col = board.col(c) 
        for r in range(board.rows-3):
            seg.append(col[r:r+4])
    for c in zip(*left_revolved):
        # slash
        for r in range(board.rows-3):
            seg.append(c[r:r+4])
    for c in zip(*right_revolved): 
        # backslash
        for r in range(board.rows-3):
            seg.append(c[r:r+4])
    # compute score
    for s in seg:
        if invalid_slot in s:
            continue
        if adversary not in s:
            score[s.count(player)] += 1
        if player not in s:
            adv_score[s.count(adversary)] += 1
    reward = sum([s*w for s, w in zip(score, weights)])
    penalty = sum([s*w for s, w in zip(adv_score, weights)])
    return reward - penalty


def minimax(player, board, depth_limit):
    """
    Minimax algorithm with limited search depth.

    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the player that needs to take an action (place a disc in the game)
    board: the current game board instance
    depth_limit: int
        the tree depth that the search algorithm needs to go further before stopping
    max_player: boolean

    Returns
    -------
    placement: int or None
        the column in which a disc should be placed for the specific player
        (counted from the most left as 0)
        None to give up the game
    """
    max_player = player
    placement = None

### Please finish the code below ##############################################
###############################################################################
    def value(player, board, depth_limit):
        # return the evaluated value if the depth limit is 0
        # or the board shows the end (draw or someone wins)
        if (depth_limit == 0 or board.terminal()):
            return evaluate(max_player, board)
        # if the player is max, run the function for a max player
        if (player == max_player):
            return max_value(player, board, depth_limit)
        # if the player is min, run the function for a min player
        else:
            return min_value(player, board, depth_limit)

    def max_value(player, board, depth_limit):
        # This is a column to place
        nonlocal placement
        # This is a score for a max player
        nonlocal score
        score = -math.inf
        # Check every possible move
        for successor in get_child_boards(player, board):
            # This allows to check with specified depth
            val = value(next_player, successor[1], depth_limit - 1)
            # Max player wants to maximize scores
            # Thus, check if the previous value is bigger than current value
            if (score < val):
                score = val
                placement = successor[0]
        return score
    
    def min_value(player, board, depth_limit):
        nonlocal placement
        nonlocal score
        score = math.inf
        for successor in get_child_boards(player, board):
            val = value(next_player, successor[1], depth_limit - 1)
            # Min player wants to minimize scores
            # Thus, check if the previous value is smaller than current value
            if (score > val):
                score = val
                placement = successor[0]
        return score

    next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
    score = -math.inf
    score = value(player, board, depth_limit)
###############################################################################
    return placement


def alphabeta(player, board, depth_limit):
    """
    Minimax algorithm with alpha-beta pruning.

     Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the player that needs to take an action (place a disc in the game)
    board: the current game board instance
    depth_limit: int
        the tree depth that the search algorithm needs to go further before stopping
    alpha: float
    beta: float
    max_player: boolean


    Returns
    -------
    placement: int or None
        the column in which a disc should be placed for the specific player
        (counted from the most left as 0)
        None to give up the game
    """
    max_player = player
    placement = None

### Please finish the code below ##############################################
###############################################################################
    def value(player, board, depth_limit):
        # return the evaluated value if the depth limit is 0
        # or the board shows the end (draw or someone wins)
        if (depth_limit == 0 or board.terminal()):
            return evaluate(player, board)
        # if the player is max, run the function for a max player
        if (next_player == max_player):
            return max_value(player, board, depth_limit)
        # if the player is min, run the function for a min player
        else:
            return min_value(player, board, depth_limit)

    def max_value(player, board, depth_limit):
        # This is a column to place
        nonlocal placement
        # This is a score for a max player
        nonlocal score
        nonlocal alpha, beta
        score = -math.inf
        # Check every possible move
        for successor in get_child_boards(player, board):
            # This allows to check with the specified depth
            val = value(player, successor[1], depth_limit - 1)
            # Max player wants to maximize scores
            # Thus, check if the previous value is bigger than current value
            if (score < val):
                score = val
                placement = successor[0]
                alpha = max(alpha, score)
            # Stop checking other child boards if beta <= alpha
            if (beta <= alpha):
                break
        return score
    
    def min_value(player, board, depth_limit):
        # This is a column to place
        nonlocal placement
        # This is a score for a max player
        nonlocal score
        nonlocal alpha, beta
        score = math.inf
        # Check every possible move
        for successor in get_child_boards(player, board):
            # This allows to check with the specified depth
            val = value(player, successor[1], depth_limit - 1)
            # Min player wants to minimize scores
            # Thus, check if the previous value is smaller than current value
            if (score > val):
                score = val
                placement = successor[0]
                beta = min(beta, score)
            # Stop checking other child boards if beta <= alpha
            if (beta <= alpha):
                break
        return score

    next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
    score = -math.inf
    alpha = -math.inf
    beta = math.inf
    score = value(player, board, depth_limit)
###############################################################################
    return placement


def expectimax(player, board, depth_limit):
    """
    Expectimax algorithm.
    We assume that the adversary of the initial player chooses actions
    uniformly at random.
    Say that it is the turn for Player 1 when the function is called initially,
    then, during search, Player 2 is assumed to pick actions uniformly at
    random.

    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the player that needs to take an action (place a disc in the game)
    board: the current game board instance
    depth_limit: int
        the tree depth that the search algorithm needs to go before stopping
    max_player: boolean

    Returns
    -------
    placement: int or None
        the column in which a disc should be placed for the specific player
        (counted from the most left as 0)
        None to give up the game
    """
    max_player = player
    placement = None

### Please finish the code below ##############################################
###############################################################################
    def value(player, board, depth_limit):
        # return the evaluated value if the depth limit is 0
        # or the board shows the end (draw or someone wins)
        if (depth_limit == 0 or board.terminal()):
            return evaluate(player, board)
        # if the player is max, run the function for a max player
        if (player == max_player):
            return max_value(player, board, depth_limit)
        # if the player is min, run the function for a min player
        else:
            return min_value(player, board, depth_limit)

    def max_value(player, board, depth_limit):
        # This is a column to place
        nonlocal placement
        # This is a score for a max player
        nonlocal score
        # Check every possible move
        for successor in get_child_boards(player, board):
            # This allows to check values with specified depth
            val = value(next_player, successor[1], depth_limit - 1)
            # Max player wants to maximize scores
            # Thus, check if the previous value is bigger than current value
            if (score < val):
                score = val
                placement = successor[0]
        return score

    def min_value(player, board, depth_limit):
        # This is a column to place
        nonlocal placement
        # This is a score for a max player
        nonlocal score
        # For expectimax with expected utility, we set initial score to zero
        score = 0
        # Check every possible move
        for successor in get_child_boards(player, board):
            #p = probability(successor)
            #score += p * value(next_player, successor[1], depth_limit - 1)
            # This allows to check values with specified depth
            val = value(next_player, successor[1], depth_limit - 1)
            # The value for probability is set to 1 / 7
            # because we always choose one from 7 options (columns) for a placement
            score += (1 / 7) * val
            # This takes values with higher probability
            if (score < val):
                score = val
                placement = successor[0]
        return score

    next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
    score = -math.inf
    score = value(player, board, depth_limit)
###############################################################################
    return placement


if __name__ == "__main__":
    from game_gui import GUI
    import tkinter

    algs = {
        "Minimax": minimax,
        "Alpha-beta pruning": alphabeta,
        "Expectimax": expectimax
    }

    root = tkinter.Tk()
    GUI(algs, root)
    root.mainloop()
