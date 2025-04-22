import streamlit as st
import numpy as np
import math
import random
import time

ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 1
AI = -1
EMPTY = 0
WINDOW_LENGTH = 4

def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(board[r][c + i] == piece for i in range(4)):
                return [(r, c + i) for i in range(4)]
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return [(r + i, c) for i in range(4)]
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return [(r + i, c + i) for i in range(4)]
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return [(r - i, c + i) for i in range(4)]
    return None

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER if piece == AI else AI
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4
    return score

def score_position(board, piece):
    score = 0
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    score += center_array.count(piece) * 3
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    return score

def get_valid_locations(board):
    return [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]

def is_terminal_node(board):
    return winning_move(board, PLAYER) or winning_move(board, AI) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    terminal = is_terminal_node(board)
    if depth == 0 or terminal:
        if terminal:
            if winning_move(board, AI):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI))
    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
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
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

# Streamlit App
st.set_page_config(page_title="Connect 4 with Minimax AI")
st.title("🎮 Connect 4 Game vs AI")

if 'board' not in st.session_state:
    st.session_state.board = create_board()
    st.session_state.game_over = False
    st.session_state.turn = PLAYER
    st.session_state.waiting_for_ai = False
    st.session_state.winner_message = None
    st.session_state.winning_positions = []

board = st.session_state.board

st.write("**Click a column number below to drop your piece.**")

cols = st.columns(COLUMN_COUNT)
for i in range(COLUMN_COUNT):
    if cols[i].button(f"⬇️ {i}", disabled=st.session_state.game_over or st.session_state.waiting_for_ai):
        if is_valid_location(board, i):
            row = get_next_open_row(board, i)
            drop_piece(board, row, i, PLAYER)
            win_positions = winning_move(board, PLAYER)
            if win_positions:
                st.session_state.winner_message = " You win! 🎉 "
                st.session_state.winning_positions = win_positions
                st.session_state.game_over = True
            else:
                st.session_state.waiting_for_ai = True
            st.rerun()

if st.session_state.winner_message:
    if "AI" in st.session_state.winner_message:
        st.error(st.session_state.winner_message)
    else:
        st.success(st.session_state.winner_message)

winning_positions = st.session_state.get("winning_positions", [])
st.write("### Board")
for r in range(ROW_COUNT-1, -1, -1):
    cols = st.columns(COLUMN_COUNT)
    for c in range(COLUMN_COUNT):
        piece = board[r][c]
        is_winning = (r, c) in winning_positions
        if piece == PLAYER:
            symbol = "🔴" if not is_winning else "🟥"
        elif piece == AI:
            symbol = "🟡" if not is_winning else "🟨"
        else:
            symbol = "⚪"
        cols[c].markdown(f"<div style='text-align:center; font-size:30px;'>{symbol}</div>", unsafe_allow_html=True)

if st.session_state.waiting_for_ai and not st.session_state.game_over:
    time.sleep(.5)
    col, _ = minimax(board, 5, -math.inf, math.inf, True)
    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, AI)
        win_positions = winning_move(board, AI)
        if win_positions:
            st.session_state.winner_message = " 💻 AI wins! 😢"
            st.session_state.winning_positions = win_positions
            st.session_state.game_over = True
    st.session_state.waiting_for_ai = False
    st.rerun()

if st.button(" Restart Game 🔄 "):
    st.session_state.board = create_board()
    st.session_state.game_over = False
    st.session_state.waiting_for_ai = False
    st.session_state.winner_message = None
    st.session_state.winning_positions = []
