import numpy as np
from numba import njit


# =============================================================================
# Helpers
# =============================================================================

@njit
def apply_move(table: np.ndarray, move_r: int, move_c: int, player: int):
    """
    Mutate table in-place: assign player to (move_r, move_c).
    Caller is responsible for passing a copy if the original must be preserved.

    # FIX 6: Original docstring claimed to return a copy but mutated in-place.
    #         Made the in-place contract explicit; callers already do .copy()
    #         before entering the MCTS loop.
    """
    table[move_r, move_c] = player
    return table


@njit
def check_winner(table: np.ndarray, root_table: np.ndarray, is_winner_player: int):
    """
    Compare cumulative payoffs after game end.
    Returns +1 if is_winner_player wins, -1 if they lose, 0 for a draw.
    """
    p1_total = 0.0
    p2_total = 0.0
    rows, cols = table.shape
    for r in range(rows):
        for c in range(cols):
            val = table[r, c]
            if val == is_winner_player:
                p1_total += root_table[r, c]
            elif val == -is_winner_player:
                p2_total += root_table[r, c]
    if p1_total > p2_total:
        return 1.0
    if p2_total > p1_total:
        return -1.0
    return 0.0


@njit
def available_moves_array_njit(table: np.ndarray, last_row: int = -1, last_col: int = -1):
    """
    Return available (row, col) pairs as an (N, 2) int32 array.

    # FIX 1: Replaced `last_move: tuple = None` with two int sentinels (-1, -1).
    #         Numba cannot express None as a default for a typed tuple argument.

    If last_row == -1  →  all free cells are candidates (opening move).
    Otherwise          →  only cells in the same row or column as last move.

    Cells are excluded when their table value is: 0 (empty/gone), -1 (blocked),
    100 (player 1 taken), or -100 (player 2 taken).
    """
    rows, cols = table.shape

    if last_row == -1:
        # No last move: every non-taken, non-blocked cell is legal
        buf = np.empty((rows * cols, 2), dtype=np.int32)
        n = 0
        for r in range(rows):
            for c in range(cols):
                v = table[r, c]
                if v != 0 and v != -1 and v != 100 and v != -100:
                    buf[n, 0] = r
                    buf[n, 1] = c
                    n += 1
        return buf[:n]
    else:
        # Only the row and column of the last move are legal
        buf = np.empty((rows + cols, 2), dtype=np.int32)
        n = 0
        # Entire row of last move
        for c in range(cols):
            v = table[last_row, c]
            if v != 0 and v != -1 and v != 100 and v != -100:
                buf[n, 0] = last_row
                buf[n, 1] = c
                n += 1
        # Entire column of last move (skip the cell already counted above)
        for r in range(rows):
            if r == last_row:
                continue
            v = table[r, last_col]
            if v != 0 and v != -1 and v != 100 and v != -100:
                buf[n, 0] = r
                buf[n, 1] = last_col
                n += 1
        return buf[:n]


# =============================================================================
# MCTS phases
# =============================================================================

@njit
def select_best_child(curr_node, legal_moves, num_cols,
                      tree_children, tree_scores, tree_visits, c_param=1.414):
    """
    Phase 1: Selection – UCB1 over fully expanded children.

    # FIX 4: `for move in legal_moves` yields a 1-D array [row, col].
    #         int(move) on a 2-element array is undefined.
    # FIX 2: tree_children is indexed by flat_idx = row * num_cols + col,
    #         not by a raw numpy row.

    Child scores are stored from the child player-to-move perspective.
    Negate them so the current parent player can maximize their own value.
    """
    best_move_r = np.int32(-1)
    best_move_c = np.int32(-1)
    best_uct    = -1e18

    parent_visits = tree_visits[curr_node]
    log_pv = np.log(parent_visits) if parent_visits > 0 else 0.0

    for i in range(len(legal_moves)):
        r        = legal_moves[i, 0]
        c        = legal_moves[i, 1]
        flat_idx = r * num_cols + c                          # FIX 2
        child    = tree_children[curr_node, flat_idx]

        cv = tree_visits[child]
        exploitation = - tree_scores[child] / cv
        exploration  = c_param * np.sqrt(log_pv / cv)
        uct          = exploitation + exploration

        if uct > best_uct:
            best_uct    = uct
            best_move_r = r
            best_move_c = c

    return best_move_r, best_move_c


@njit
def run_simulation(sim_state, beginning_player: int,
                   root_table: np.ndarray,
                   start_last_row: int = -1, start_last_col: int = -1):
    """
    Phase 3: Rollout – random play-out to terminal state.

    # FIX 1: last_move tuple → two int arguments with -1 sentinel.

    Returns +1 if beginning_player wins, -1 if they lose, 0 for draw.
    """
    player        = beginning_player
    cur_last_row  = start_last_row
    cur_last_col  = start_last_col

    while True:
        moves = available_moves_array_njit(sim_state, cur_last_row, cur_last_col)
        if len(moves) == 0:
            break
        idx          = np.random.randint(len(moves))
        mr, mc       = moves[idx, 0], moves[idx, 1]
        apply_move(sim_state, mr, mc, player)
        cur_last_row = mr
        cur_last_col = mc
        player       = -player

    return check_winner(sim_state, root_table, beginning_player)


@njit
def backpropagate(curr_node, payoff, tree_parents, tree_visits, tree_scores):
    """
    Phase 4: Walk from curr_node to root, updating stats.

    NEGAMAX convention (FIX 5):
    ────────────────────────────
    Each node stores the score from the perspective of the player who is
    ABOUT TO MOVE from that node.  When we climb from child to parent the
    turn flips, so the payoff sign flips too.

    With this convention select_best_child can *always* maximise without
    knowing which player sits at a node – correct for both players.

    Original bug: a payoff was pre-adjusted to root_player's absolute frame
    before backprop, but backprop then *also* inverted at every level →
    parent nodes maximised the wrong direction.
    """
    current_payoff = payoff
    node = curr_node
    while node != -1:
        tree_visits[node] += 1
        tree_scores[node] += current_payoff
        current_payoff     = -current_payoff   # flip for parent's perspective
        node               = tree_parents[node]


# =============================================================================
# Main search
# =============================================================================

@njit
def mcts_search(root_state: np.ndarray, iterations: int,
                root_player: int, max_moves: int,
                root_last_row: int = -1, root_last_col: int = -1):
    """
    Run MCTS and return (best_row, best_col).

    # FIX 1: root_last_move tuple → root_last_row / root_last_col ints.
    # FIX 7: max_nodes increased from iterations+10 to iterations*2+10
    #         so the pool survives if expansion ever adds multiple nodes.

    Returns (-1, -1) if no legal move exists at the root.
    """
    rows, cols = root_state.shape
    num_cols   = cols
    max_nodes  = iterations * 2 + 10                         # FIX 7

    # Pre-allocated tree arrays
    tree_visits   = np.zeros(max_nodes, dtype=np.int32)
    tree_scores   = np.zeros(max_nodes, dtype=np.float32)
    tree_parents  = np.full(max_nodes, -1, dtype=np.int32)
    tree_children = np.full((max_nodes, max_moves), -1, dtype=np.int32)

    node_count = 1   # node 0 is the root

    for _ in range(iterations):
        curr_node      = 0
        state          = root_state.copy()
        player         = root_player
        cur_last_row   = root_last_row
        cur_last_col   = root_last_col

        # ── PHASE 1 & 2: SELECTION & EXPANSION ───────────────────────────
        while True:
            legal_moves = available_moves_array_njit(state, cur_last_row, cur_last_col)

            if len(legal_moves) == 0:
                break   # terminal node inside the tree

            # FIX 3: collect unexpanded moves into a pre-allocated buffer
            #         instead of a Python list of numpy arrays (unreliable in numba).
            # FIX 2: use flat index to look up tree_children.
            unexpanded_buf = np.empty((len(legal_moves), 2), dtype=np.int32)
            n_unexpanded   = 0
            for i in range(len(legal_moves)):
                r        = legal_moves[i, 0]
                c        = legal_moves[i, 1]
                flat_idx = r * num_cols + c                  # FIX 2
                if tree_children[curr_node, flat_idx] == -1:
                    unexpanded_buf[n_unexpanded, 0] = r
                    unexpanded_buf[n_unexpanded, 1] = c
                    n_unexpanded += 1

            if n_unexpanded > 0:
                # EXPANSION: pick a random unexpanded move
                idx      = np.random.randint(n_unexpanded)
                chosen_r = unexpanded_buf[idx, 0]
                chosen_c = unexpanded_buf[idx, 1]
                flat_idx = chosen_r * num_cols + chosen_c    # FIX 2

                apply_move(state, chosen_r, chosen_c, player)

                new_node = node_count
                node_count += 1
                tree_parents[new_node]                  = curr_node
                tree_children[curr_node, flat_idx]      = new_node  # FIX 2

                curr_node    = new_node
                player       = -player
                cur_last_row = chosen_r
                cur_last_col = chosen_c
                break   # proceed to simulation from newly expanded node

            else:
                # SELECTION: all children exist – descend via UCB1
                best_r, best_c = select_best_child(
                    curr_node, legal_moves, num_cols,
                    tree_children, tree_scores, tree_visits, c_param=1.41
                )
                flat_idx  = best_r * num_cols + best_c      # FIX 2
                apply_move(state, best_r, best_c, player)
                curr_node    = tree_children[curr_node, flat_idx]
                player       = -player
                cur_last_row = best_r
                cur_last_col = best_c

        # ── PHASE 3: SIMULATION ───────────────────────────────────────────
        # FIX 5 (negamax): simulate from the perspective of whoever moves next.
        # No pre-adjustment to root_player's frame — backprop handles everything.
        payoff = run_simulation(
            state, player, root_state,
            start_last_row=cur_last_row,
            start_last_col=cur_last_col
        )

        # ── PHASE 4: BACKPROPAGATION ──────────────────────────────────────
        backpropagate(curr_node, payoff, tree_parents, tree_visits, tree_scores)

    # ── Pick the root child with the most visits ──────────────────────────
    root_legal = available_moves_array_njit(root_state, root_last_row, root_last_col)
    best_move_r = np.int32(-1)
    best_move_c = np.int32(-1)
    max_v       = -1

    for i in range(len(root_legal)):
        r        = root_legal[i, 0]
        c        = root_legal[i, 1]
        flat_idx = r * num_cols + c                          # FIX 2
        child    = tree_children[0, flat_idx]
        if child != -1 and tree_visits[child] > max_v:
            max_v       = tree_visits[child]
            best_move_r = r
            best_move_c = c

    return best_move_r, best_move_c
