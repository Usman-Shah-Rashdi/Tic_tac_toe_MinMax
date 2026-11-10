# Tic-Tac-Toe Minimax

A desktop Tic-Tac-Toe game built with [Pygame](https://www.pygame.org/). Play
against an unbeatable computer opponent powered by the minimax algorithm.

## Features

- 3x3 graphical game board
- Human player uses circles (`1`)
- Computer player uses crosses (`2`)
- Computer chooses moves with minimax
- Automatic win and draw detection
- Press `R` to restart the game

## Requirements

- Python 3
- Pygame
- Pytest (only required for running the tests)

## Installation

Clone the repository and install the dependencies:

```bash
git clone <repository-url>
cd Tic_tac_toe_MinMax
python -m pip install pygame pytest
```

Using a virtual environment is recommended:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install pygame pytest
```

On Windows, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Run the game

```bash
python Tic_tac_toe.py
```

Click an empty square to place your circle. The computer responds
automatically with its cross. Close the window to exit, or press `R` to clear
the board and start a new game.

## Run the tests

```bash
python -m pytest
```

The tests cover winner detection, full-board detection, minimax scoring,
blocking an immediate opponent win, and the AI's opening move.

## Project structure

```text
.
├── Tic_tac_toe.py
└── tests/
    └── test_tic_tac_toe.py
```

The game logic is kept in `Tic_tac_toe.py`. The `minimax` and `ai_move`
functions evaluate moves without drawing to the screen, which also allows the
logic to be tested independently of the graphical interface.
