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
# Set the window size
SQUARE_SIZE = 100
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
size = (width, height)
# for circles
RADIUS = int(SQUARE_SIZE / 2 - 5)



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

#must edit to connect 6
def winning_move(board, piece):
    # Check all horizontal location
    for c in range(COLUMN_COUNT - 5):  # because theres no 6 in the last 5
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and \
                    board[r][c + 2] == piece and board[r][c + 3] == piece\
                    and board[r][c+4] == piece and board[r][c+5] == piece:
                return True

    # Check vertical locations
    for c in range(COLUMN_COUNT):  # because theres no 4 in the last 3
        for r in range(ROW_COUNT - 5):
            if board[r][c] == piece and board[r + 1][c] == piece and \
                    board[r + 2][c] == piece and board[r + 3][c] == piece\
                    and board[r+4][c] == piece and board[r+5][c] == piece:
                return True

    # Check + diagonals
    for c in range(COLUMN_COUNT - 5):  # because theres no 6 in the last 6
        for r in range(ROW_COUNT - 5):
            if board[r][c] == piece and board[r+1][c+1] == piece and \
                    board[r+2][c+2] == piece and board[r+3][c+3] == piece\
                    and board[r+4][c+4] == piece and board[r+5][c+5] == piece:
                return True

    # Check - diagonals
    for c in range(COLUMN_COUNT - 5):  # because theres no 4 in the last 3
        for r in range(5, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and \
                    board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece\
                    and board[r-4][c+4] == piece and board[r-5][c+5] == piece:
                return True


def draw_board(board, screen):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # Where, color, width, height, position x2
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                               int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                                 height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                                    height - int(r * SQUARE_SIZE +
                                                                 SQUARE_SIZE / 2)), RADIUS)

    pygame.display.update()


def run():
    board = create_board()
    game_over = False
    turn = 0

    pygame.init()

    # Create the screen and update
    screen = pygame.display.set_mode(size)

    draw_board(board, screen)
    pygame.display.update()
    # Create font
    my_font = pygame.font.SysFont("monospace", 75)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                pos_x = event.pos[0]
                if turn % 2 == 0:
                    pygame.draw.circle(screen, RED, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                # Ask for player 1 input
                if turn % 2 == 0:
                    pos_x = event.pos[0]
                    col = int(math.floor(pos_x / SQUARE_SIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            label = my_font.render("Player 1 Wins!", 1, RED)
                            screen.blit(label, (120, 10))
                            game_over = True

                # Ask for player 2 input
                else:
                    pos_x = event.pos[0]
                    col = int(math.floor(pos_x / SQUARE_SIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            label = my_font.render("Player 2 Wins!", 1, YELLOW)
                            screen.blit(label, (120, 10))
                            game_over = True

                draw_board(board, screen)
                turn += 1

                if game_over:
                    pygame.time.wait(2000)
