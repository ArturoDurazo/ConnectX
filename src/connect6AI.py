import random
import numpy as np
import pygame
import sys
import math

ROW_COUNT = 8
COLUMN_COUNT = 9

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 6

# Set the window size
SQUARE_SIZE = 100
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
size = (width, height)
# for circles
RADIUS = int(SQUARE_SIZE / 2 - 5)


# COULD TRY TO MAKE THE BOARD SIZE DYNAMIC AND MAYBE DO CONNECT 6 or so?

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check all horizontal location
    for c in range(COLUMN_COUNT - 5):  # because theres no 6 in the last 5
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and \
                    board[r][c + 2] == piece and board[r][c + 3] == piece \
                    and board[r][c+4] == piece and board[r][c+5] == piece:
                return True

    # Check vertical locations
    for c in range(COLUMN_COUNT):  # because theres no 4 in the last 3
        for r in range(ROW_COUNT - 5):
            if board[r][c] == piece and board[r + 1][c] == piece and \
                    board[r + 2][c] == piece and board[r + 3][c] == piece \
                    and board[r+4][c] == piece and board[r+5][c] == piece:
                return True

    # Check + diagonals
    for c in range(COLUMN_COUNT - 5):  # because theres no 6 in the last 6
        for r in range(ROW_COUNT - 5):
            if board[r][c] == piece and board[r+1][c+1] == piece and \
                    board[r+2][c+2] == piece and board[r+3][c+3] == piece \
                    and board[r+4][c+4] == piece and board[r+5][c+5] == piece:
                return True

    # Check - diagonals
    for c in range(COLUMN_COUNT - 5):  # because theres no 4 in the last 3
        for r in range(5, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and \
                    board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece \
                    and board[r-4][c+4] == piece and board[r-5][c+5] == piece:
                return True


def evaluate_window(window, piece):
    score = 0
    opponent_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE
    #irrelevant unless depth = 0 because now it can look into the future with minimax
    if window.count(piece) == 6:
        score += 1000
    elif window.count(piece) == 5 and window.count(EMPTY) == 1:
        score += 100
    elif window.count(piece) == 4 and window.count(EMPTY) == 2:
        score += 80
    elif window.count(piece) == 3 and window.count(EMPTY) == 2:
        score += 40
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 20
    #irrelevant unless depth = 0 because now it can look into the future with minimax
    if window.count(opponent_piece) == 5 and window.count(EMPTY) == 1:
        score -= 4

    return score


def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def score_position(board, piece):
    score = 0
    #Center Score
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    #Horizontal Score
    #For winning +100 points
    for r in range(ROW_COUNT):
        #Grabs a single row and drops it into an array so we can count how many pieces there are
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 5):
            #count in windows of 6 but skip the last 5
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    #Vertical Score
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 5):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    #Diagonal +
    for r in range(ROW_COUNT - 5):
        for c in range(COLUMN_COUNT - 5):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    #Diagonal -
    for r in range(ROW_COUNT - 5):
        for c in range(COLUMN_COUNT - 5):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return None, 10000000000000000000000
            elif winning_move(board, PLAYER_PIECE):
                return None, -10000000000000000000000
            else: #Game is dead
                return None, 0
        else: #depth is zero
            return None, score_position(board, AI_PIECE)

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


#Get a list of valid location where the AI can drop a piece
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def draw_board(board, screen):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # Where, color, width, height, position x2
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                               int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                                 height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                                    height - int(r * SQUARE_SIZE +
                                                                 SQUARE_SIZE / 2)), RADIUS)

    pygame.display.update()

def run(diff):
    board = create_board()
    game_over = False

    pygame.init()

    # Create the screen and update
    screen = pygame.display.set_mode(size)

    draw_board(board, screen)
    pygame.display.update()
    # Create font
    my_font = pygame.font.SysFont("monospace", 75)

    #this way whoever starts is random
    turn = random.randint(PLAYER, AI)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                pos_x = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                # Ask for player 1 input
                if turn == PLAYER:
                    pos_x = event.pos[0]
                    col = int(math.floor(pos_x / SQUARE_SIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            label = my_font.render("Player 1 Wins!", 1, RED)
                            screen.blit(label, (120, 10))
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        print_board(board)
                        draw_board(board, screen)

        # Ask for player 2 input
        if turn == AI and not game_over:
            col, minimax_score = minimax(board, diff, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = my_font.render("Player 2 Wins!", 1, YELLOW)
                    screen.blit(label, (120, 10))
                    game_over = True

                draw_board(board, screen)
                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(2000)
