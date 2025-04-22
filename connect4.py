import streamlit as st
import numpy as np
import math
import random
import time

ROW_COUNT = 6
COL_COUNT = 7
PLAYER = 1
AI = -1
EMPTY = 0
WIN_LEN = 4

# empty board
def create_board():
    return np.zeros((ROW_COUNT, COL_COUNT), dtype=int)

# Drop a piece into the board 
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Check top column is  empty
def valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

# Get next row in a column
def getnextrow(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Check player win
def win_move(board, piece):
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(board[r][c + i] == piece for i in range(4)):
                return [(r, c + i) for i in range(4)]
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return [(r + i, c) for i in range(4)]
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return [(r + i, c + i) for i in range(4)]
    for c in range(COL_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return [(r - i, c + i) for i in range(4)]

    return None

def Window(window, piece):
    score = 0
    opp = PLAYER if piece == AI else AI

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_point(board, piece):
    score = 0

    center = [int(i) for i in list(board[:, COL_COUNT // 2])]
    score += center.count(piece) * 3
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COL_COUNT - 3):
            window = row_array[c:c + WIN_LEN]
            score += Window(window, piece)
    for c in range(COL_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WIN_LEN]
            score += Window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COL_COUNT - 3):
            diag1 = [board[r + i][c + i] for i in range(WIN_LEN)]
            diag2 = [board[r + 3 - i][c + i] for i in range(WIN_LEN)]
            score += Window(diag1, piece)
            score += Window(diag2, piece)

    return score

def valid_point(board):
    return [c for c in range(COL_COUNT) if valid_location(board, c)]

def term_node(board):
    return win_move(board, PLAYER) or win_move(board, AI) or len(valid_point(board)) == 0

# Minimax with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizePlayer):
    valid_locations = valid_point(board)
    terminal = term_node(board)

    if depth == 0 or terminal:
        if terminal:
            if win_move(board, AI):
                return (None, 1000)
            elif win_move(board, PLAYER):
                return (None, -1000)
            else:
                return (None, 0)
        else:
            return (None, score_point(board, AI))

    if maximizePlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = getnextrow(board, col)
            temp = board.copy()
            drop_piece(temp, row, col, AI)
            new_score = minimax(temp, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value

    else:
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = getnextrow(board, col)
            temp = board.copy()
            drop_piece(temp, row, col, PLAYER)
            new_score = minimax(temp, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

# Streamlit GUI
st.set_page_config(page_title="Connect 4 with Minimax Algo")
st.title("Connect 4 Game vs AI")

if 'board' not in st.session_state:
    st.session_state.board = create_board()
    st.session_state.turn = PLAYER
    st.session_state.game_over = False
    st.session_state.waiting_for_ai = False
    st.session_state.winner_message = None
    st.session_state.winning_positions = []

board = st.session_state.board

st.write("Click a column number to drop your piece.")

cols = st.columns(COL_COUNT)
for i in range(COL_COUNT):
    if cols[i].button(f"⬇️ {i}", disabled=st.session_state.game_over or st.session_state.waiting_for_ai):
        if valid_location(board, i):
            row = getnextrow(board, i)
            drop_piece(board, row, i, PLAYER)
            win_pos = win_move(board, PLAYER)
            if win_pos:
                st.session_state.winner_message = " You win! 🎉 "
                st.session_state.winning_positions = win_pos
                st.session_state.game_over = True
            else:
                st.session_state.waiting_for_ai = True
            st.rerun()

if st.session_state.winner_message:
    if "AI" in st.session_state.winner_message:
        st.error(st.session_state.winner_message)
    else:
        st.success(st.session_state.winner_message)

# board
st.write("### Current Board")
win_pos = st.session_state.get("winning_positions", [])
for r in range(ROW_COUNT - 1, -1, -1):
    row = st.columns(COL_COUNT)
    for c in range(COL_COUNT):
        piece = board[r][c]
        is_win = (r, c) in win_pos
        if piece == PLAYER:
            emoji = "🔴" if not is_win else "🟥"
        elif piece == AI:
            emoji = "🟡" if not is_win else "🟨"
        else:
            emoji = "⚪"
        row[c].markdown(f"<div style='text-align:center; font-size:30px;'>{emoji}</div>", unsafe_allow_html=True)

# AI Move
if st.session_state.waiting_for_ai and not st.session_state.game_over:
    time.sleep(0.5) 
    col, _ = minimax(board, 5, -math.inf, math.inf, True)
    if valid_location(board, col):
        row = getnextrow(board, col)
        drop_piece(board, row, col, AI)
        win_pos = win_move(board, AI)
        if win_pos:
            st.session_state.winner_message = " 💻 AI wins! 😢"
            st.session_state.winning_positions = win_pos
            st.session_state.game_over = True
    st.session_state.waiting_for_ai = False
    st.rerun()

# Reset button
if st.button(" Restart Game 🔄 "):
    st.session_state.board = create_board()
    st.session_state.turn = PLAYER
    st.session_state.game_over = False
    st.session_state.waiting_for_ai = False
    st.session_state.winner_message = None
    st.session_state.winning_positions = []
