"""function minimax(position, depth, alpha, beta, maximizingPlayer)
    if depth == 0 or game over in position:
        return static evaluation of position

    if maximizingPlayer:
        maxEval = -infinity
        for each child of position
            eval = minimax(child, depth - 1, alpha, beta false)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval

    else:
        minEval = +infinity
        for each child of position
            eval = minimax(child, depth - 1, alpha, beta true)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval


// initial call
minimax(currentPosition, 3, -∞, +∞, true)

"""
def minimax (state, depth, player):
    """
    :param state: state of the board
    :param depth: index of node
    :param player: currently Maximizing or Minimizing player
    :return:
    """
    if depth == 0 or game_over(state)
        score = evaluate(state)
        return score




def compare_score (player, score, best):
    if player == True:
        if score > best:
            best = score
    else:
        if score < best:
            best = score