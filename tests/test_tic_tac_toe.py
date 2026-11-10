import builtins
import types
import pygame
import pytest

import Tic_tac_toe as ttt


@pytest.fixture(autouse=True)
def reset_board_monkeypatch(monkeypatch):
    # Ensure a clean board for each test and stub out drawing calls
    ttt.board = [[0 for _ in range(ttt.BOARD_COLS)] for _ in range(ttt.BOARD_ROWS)]

    class DummySurface:
        def fill(self, *args, **kwargs):
            pass

    # Provide a dummy screen surface to allow draw calls without real display
    ttt.screen = DummySurface()

    # Monkeypatch pygame.draw methods to be no-ops
    monkeypatch.setattr(pygame.draw, 'line', lambda *args, **kwargs: None)
    monkeypatch.setattr(pygame.draw, 'circle', lambda *args, **kwargs: None)


# Behaviors
# 1) evaluate_winner should detect all win directions for either player
# 2) board_full should return True when no zeros remain and False otherwise
# 3) minimax should score +1 for AI (player 2) win, -1 for human (player 1) win, 0 for draw
# 4) minimax should choose blocking move when opponent threatens immediate win
# 5) ai_move should select center when available on empty board (optimal first move)


def test_evaluate_winner_detects_rows_cols_diagonals():
    # Row win for player 1
    b = [
        [1, 1, 1],
        [0, 2, 0],
        [2, 0, 0],
    ]
    assert ttt.evaluate_winner(b) == 1

    # Column win for player 2
    b = [
        [2, 1, 0],
        [2, 1, 0],
        [2, 0, 1],
    ]
    assert ttt.evaluate_winner(b) == 2

    # Asc diagonal win for player 1
    b = [
        [2, 0, 1],
        [0, 1, 0],
        [1, 2, 2],
    ]
    assert ttt.evaluate_winner(b) == 1

    # Desc diagonal win for player 2
    b = [
        [2, 1, 0],
        [1, 2, 1],
        [0, 0, 2],
    ]
    assert ttt.evaluate_winner(b) == 2

    # No winner
    b = [
        [2, 1, 2],
        [1, 2, 1],
        [1, 2, 1],
    ]
    assert ttt.evaluate_winner(b) == 0


def test_board_full_true_false():
    full = [
        [1, 2, 1],
        [2, 1, 2],
        [2, 1, 2],
    ]
    assert ttt.board_full(full) is True

    not_full = [
        [1, 0, 1],
        [0, 1, 2],
        [2, 1, 0],
    ]
    assert ttt.board_full(not_full) is False


def test_minimax_scores_terminal_states():
    # AI (2) has a win
    ai_win = [
        [2, 2, 2],
        [1, 1, 0],
        [0, 0, 0],
    ]
    assert ttt.minimax([row[:] for row in ai_win], 0, True) == 1

    # Human (1) has a win
    human_win = [
        [1, 1, 1],
        [2, 2, 0],
        [0, 0, 0],
    ]
    assert ttt.minimax([row[:] for row in human_win], 0, False) == -1

    # Draw board
    draw = [
        [1, 2, 1],
        [1, 2, 2],
        [2, 1, 1],
    ]
    assert ttt.minimax([row[:] for row in draw], 0, True) == 0


def test_minimax_blocks_immediate_opponent_win():
    # Human (1) threatens to win next move on row 0 at col 2 -> AI must block
    b = [
        [1, 1, 0],
        [0, 2, 0],
        [0, 0, 0],
    ]
    best_score = -float('inf')
    best_move = None
    for r in range(ttt.BOARD_ROWS):
        for c in range(ttt.BOARD_COLS):
            if b[r][c] == 0:
                b[r][c] = 2
                score = ttt.minimax(b, 0, False)
                b[r][c] = 0
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
    assert best_move == (0, 2)


def test_ai_move_picks_center_on_empty_board():
    # Empty board -> center is optimal
    for r in range(ttt.BOARD_ROWS):
        for c in range(ttt.BOARD_COLS):
            ttt.board[r][c] = 0
    # ensure game_over exists
    ttt.game_over = False

    # run ai move
    ttt.ai_move()

    assert ttt.board[1][1] == 2, "AI should take the center square on empty board"
