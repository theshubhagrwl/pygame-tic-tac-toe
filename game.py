import pygame
from tkinter import *
from tkinter import messagebox


# Colours
BLACK = (0, 0, 0)
WHITE = (225, 255, 255)
GREEN = (25, 207, 34)

# Variables for board
ROWS = 3
COLS = 3
BOX_SIZE = 100
LINE_WIDTH = 8
WINDOW_WIDTH = 440
WINDOW_HEIGHT = 440

# Starting co-ordinates of the board
x = 70
y = 80

# Rectangle overlays on the board
rec1 = pygame.Rect(x, y, BOX_SIZE, BOX_SIZE)
rec2 = pygame.Rect(x+BOX_SIZE, y, BOX_SIZE, BOX_SIZE)
rec3 = pygame.Rect(x+(2*BOX_SIZE), y, BOX_SIZE, BOX_SIZE)
rec4 = pygame.Rect(x, y+BOX_SIZE, BOX_SIZE, BOX_SIZE)
rec5 = pygame.Rect(x+BOX_SIZE, y+BOX_SIZE, BOX_SIZE, BOX_SIZE)
rec6 = pygame.Rect(x+(2*BOX_SIZE), y+BOX_SIZE, BOX_SIZE, BOX_SIZE)
rec7 = pygame.Rect(x, y+(2*BOX_SIZE), BOX_SIZE, BOX_SIZE)
rec8 = pygame.Rect(x+BOX_SIZE, y+(2*BOX_SIZE), BOX_SIZE, BOX_SIZE)
rec9 = pygame.Rect(x+(2*BOX_SIZE), y+(2*BOX_SIZE), BOX_SIZE, BOX_SIZE)

rectangles = [[rec1, rec2, rec3], [rec4, rec5, rec6], [rec7, rec8, rec9]]


def main():
    global CLOCK, SCREEN
    board = [[False, False, False], [
        False, False, False], [False, False, False]]

    usedBox = [[False, False, False], [
        False, False, False], [False, False, False]]
    pygame.init()
    CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("TIC TAC TOE")
    SCREEN.fill(BLACK)

    markFont = pygame.font.SysFont("Helvetica", 110)
    smallFont = pygame.font.Font("freesansbold.ttf", 26)

    mouse_x = 0
    mouse_y = 0

    player1TurnDone = False

    player1Score = 0
    player2Score = 0
    tieScore = 0
    player1Wins = False
    player2Wins = False

    drawBoard()

    while True:

        mouseClicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouseClicked = True

        box_x, box_y = getRectAtMousePos(mouse_x, mouse_y)

        if box_x != None and box_y != None:
            if usedBox[box_x][box_y] == False and mouseClicked == False and player1TurnDone == False:
                markX(box_x, box_y, markFont)
                usedBox[box_x][box_y] = True
                board[box_x][box_y] = "X"
                player1TurnDone = True
                pygame.display.update()

            elif player1TurnDone == True and usedBox[box_x][box_y] == False:
                markO(box_x, box_y, markFont)
                usedBox[box_x][box_y] = True
                board[box_x][box_y] = "O"
                player1TurnDone = False
                pygame.display.update()

        player1Wins, player2Wins = check_for_victory(board)

        if player1Wins:
            pygame.time.wait(500)
            player1Score += 1
            board, usedBox, player1TurnDone, player1Wins, player2Wins = reset(
                board, usedBox, player1TurnDone, player1Wins, player2Wins)
            msg = "Player 1 is the WINNNER! \nPress ENTER to continue"
            box(msg)
            SCREEN.fill(BLACK)
            pygame.mouse.set_pos(x-10, y-10)
            drawBoard()

        elif player2Wins:
            pygame.time.wait(500)
            player2Score += 1
            board, usedBox, player1TurnDone, player1Wins, player2Wins = reset(
                board, usedBox, player1TurnDone, player1Wins, player2Wins)
            msg = "Player 2 is the WINNNER! \nPress ENTER to continue"
            box(msg)
            SCREEN.fill(BLACK)
            pygame.mouse.set_pos(x-10, y-10)
            drawBoard()

        else:
            if gameOver(usedBox, board):
                tieScore += 1
                board, usedBox, player1TurnDone, player1Wins, player2Wins = reset(
                    board, usedBox, player1TurnDone, player1Wins, player2Wins)
                msg = "It's a TIE! Give it another try.\nPress ENTER to continue"
                box(msg)
                SCREEN.fill(BLACK)
                pygame.mouse.set_pos(x-10, y-10)
                drawBoard()

        # Print score
        drawScoreBoard(smallFont, player1Score, player2Score, tieScore)

        pygame.display.update()
        CLOCK.tick(60)


def drawBoard():
    # Vertical Lines
    pygame.draw.rect(SCREEN, WHITE,
                     pygame.Rect(x+BOX_SIZE, y, LINE_WIDTH, 300))
    pygame.draw.rect(SCREEN, WHITE,
                     pygame.Rect(x+(2*BOX_SIZE), y, LINE_WIDTH, 300))
    # Horizontal lines
    pygame.draw.rect(SCREEN, WHITE,
                     pygame.Rect(x, y+BOX_SIZE, 300, LINE_WIDTH))
    pygame.draw.rect(SCREEN, WHITE, pygame.Rect(
        x, y+(2*BOX_SIZE), 300, LINE_WIDTH))


def getRectAtMousePos(mouse_x, mouse_y):
    for box_x in range(COLS):
        for box_y in range(ROWS):
            boxRect = rectangles[box_x][box_y]
            if boxRect.collidepoint(mouse_x, mouse_y):
                return(box_x, box_y)
    return(None, None)


def markX(box_x, box_y, markFont):
    mark = markFont.render("X", True, WHITE)
    markRect = rectangles[box_x][box_y]
    if box_x == 0:
        markRect.x += 10
        markRect.y -= 10
        SCREEN.blit(mark, markRect)
        markRect.x -= 10
        markRect.y += 10

    elif box_x == 1:
        markRect.x += 7
        markRect.y -= 5
        SCREEN.blit(mark, markRect)
        markRect.x -= 7
        markRect.y += 5
    elif box_x == 2:
        markRect.x += 10
        SCREEN.blit(mark, markRect)
        markRect.x -= 10
    else:
        SCREEN.blit(mark, markRect)


def markO(box_x, box_y, markFont):
    mark = markFont.render("O", True, WHITE)
    markRect = rectangles[box_x][box_y]
    if box_x == 0:
        markRect.x += 10
        markRect.y -= 10
        SCREEN.blit(mark, markRect)
        markRect.x -= 10
        markRect.y += 10
    elif box_x == 1:
        markRect.x += 7
        markRect.y -= 5
        SCREEN.blit(mark, markRect)
        markRect.x -= 7
        markRect.y += 5
    elif box_x == 2:
        markRect.x += 10
        SCREEN.blit(mark, markRect)
        markRect.x -= 10
    else:
        SCREEN.blit(mark, markRect)


def check_for_victory(board):
    if ((board[0][0] == board[1][0] == board[2][0] == "X") or
        (board[0][1] == board[1][1] == board[2][1] == "X") or
        (board[0][2] == board[1][2] == board[2][2] == "X") or
        (board[0][0] == board[0][1] == board[0][2] == "X") or
        (board[1][0] == board[1][1] == board[1][2] == "X") or
        (board[2][0] == board[2][1] == board[2][2] == "X") or
        (board[0][0] == board[1][1] == board[2][2] == "X") or
            (board[0][2] == board[1][1] == board[2][0] == "X")):

        player1Wins = True
        player2Wins = False
        return player1Wins, player2Wins

    elif ((board[0][0] == board[1][0] == board[2][0] == "O") or
          (board[0][1] == board[1][1] == board[2][1] == "O") or
          (board[0][2] == board[1][2] == board[2][2] == "O") or
          (board[0][0] == board[0][1] == board[0][2] == "O") or
          (board[1][0] == board[1][1] == board[1][2] == "O") or
          (board[2][0] == board[2][1] == board[2][2] == "O") or
          (board[0][0] == board[1][1] == board[2][2] == "O") or
            (board[0][2] == board[1][1] == board[2][0] == "O")):

        player1Wins = False
        player2Wins = True
        return player1Wins, player2Wins

    else:
        player1Wins = False
        player2Wins = False
        return player1Wins, player2Wins


def reset(board, usedBox, player1TurnDone, player1Wins, player2Wins):
    board = [[False, False, False], [
        False, False, False], [False, False, False]]
    usedBox = [[False, False, False], [
        False, False, False], [False, False, False]]
    player1TurnDone = False
    player1Wins = False
    player2Wins = False
    return board, usedBox, player1TurnDone, player1Wins, player2Wins


def gameOver(usedBox, board):
    for boxx in range(COLS):
        for boxy in range(ROWS):
            if usedBox[boxx][boxy] == False:
                return False

    else:
        return True


def drawScoreBoard(smallFont, player1Score, player2Score, tieScore):
    scoreBoard = smallFont.render('Player 1: ' + str(player1Score) + '     ' + 'Player 2: ' + str(
        player2Score) + '      ' + 'Tie: ' + str(tieScore), True, GREEN, BLACK)
    scoreBoardRect = scoreBoard.get_rect()
    scoreBoardRect.x = 10
    scoreBoardRect.y = 10
    SCREEN.blit(scoreBoard, scoreBoardRect)


def box(msg):
    Tk().wm_withdraw()
    messagebox.showinfo("CONGRATS!", msg)


if __name__ == '__main__':
    main()
