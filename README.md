# Connect 4 Game with AI

A Python implementation of the classic Connect 4 game featuring an AI opponent using the Minimax algorithm with alpha-beta pruning.

![Connect 4 Game Screenshot](https://imgur.com/a/xujXEd3)

## Features

- Classic Connect 4 gameplay (6 rows × 7 columns)
- AI opponent using Minimax algorithm with alpha-beta pruning
- Score-based position evaluation
- Interactive web interface using Streamlit
- Visual indicators for winning moves
- Game restart functionality

## How to Play

1. Click on any column number to drop your red piece (🔴)
2. The AI will automatically respond with its yellow piece (🟡)
3. Connect four of your pieces horizontally, vertically, or diagonally to win
4. Use the "Restart Game" button to start a new game at any time

## Installation

1. Ensure you have Python 3.7+ installed
2. Install the required packages:
pip install streamlit numpy

3. Run the game:
streamlit run connect4.py


## Game Rules

- Players take turns dropping pieces into columns
- Pieces fall to the lowest available space in the column
- The first player to connect four of their pieces wins
- The game ends in a draw if the board fills without a winner

## AI Implementation

The AI uses:
- Minimax algorithm with alpha-beta pruning for decision making
- Depth-limited search (currently set to depth 6)
- Position evaluation based on:
- Potential winning moves
- Center control
- Piece configurations (3 in a row, 2 in a row)
- Blocking opponent's potential wins

## Customization

You can adjust game parameters in the code:
- `ROW_COUNT` and `COLUMN_COUNT` for board size
- `WINDOW_LENGTH` for connection length (default 4)
- Minimax depth for AI difficulty

## Requirements

- Python 3.7+
- Streamlit
- NumPy

## License

This project is open source and available under the MIT License.
