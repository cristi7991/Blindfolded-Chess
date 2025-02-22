import pygame
import os
from copy import copy, deepcopy

whitePieces = {'Rw', 'Nw', 'Bw', 'Kw', 'Qw', 'Pw'}
blackPieces = {'Rb', 'Nb', 'Bb', 'Kb', 'Qb', 'Pb'}

def getColor(x, y):
# -1 empty, 0 white, 1 black

    if board[x][y] == 0:
        return -1
    if board[x][y] in whitePieces:
        return 0
    return 1

def getPieceImage(x):

    if x == 'Kw':       #king
        return [0,0]
    if x == 'Qw':       #queen
        return [square_width, 0]
    if x == 'Bw':       #bishop
        return [2 * square_width, 0]
    if x == 'Nw':       #knight
        return [3 * square_width, 0]
    if x == 'Rw':       #rook
        return [4 * square_width, 0]
    if x == 'Pw':       #pawn
        return [5 * square_width, 0]

    if x == 'Kb':       #king
        return [0, square_height]
    if x == 'Qb':       #queen
        return [square_width, square_height]
    if x == 'Bb':       #bishop
        return [2 * square_width, square_height]
    if x == 'Nb':       #knight
        return [3 * square_width, square_height]
    if x == 'Rb':       #rook
        return [4 * square_width, square_height]
    if x == 'Pb':       #pawn
        return [5 * square_width, square_height]



def drawBoard():
    #Blit the background:
    if boardWithHelp:
        screen.blit(background1, (0, 0))
    else:
        screen.blit(background2, (0, 0))
    if showTable:
        for i in range(8):
            for j in range(8):
                if board[i][j] != 0:
                    [x,y] = getPieceImage(board[i][j])
                    screen.blit(pieces_image, (j * square_width, i * square_height),
                                                (x, y, square_width, square_height))

def checkValidWhitePawnMove(x1, y1, x2, y2):

    ok = 0
    if y1 == y2:
        if x1 == 6:
            if x2 != 5 and x2 != 4:
                ok = 1
            if board[x2][y2] != 0:
                ok = 1
            if x2 == 4 and board[5][y2] != 0:
                ok = 1
        else:
            if x1 - x2 != 1:
                ok = 1
            if board[x2][y2] != 0:
                ok = 1
    else:
        if x1 - x2 == 1:
            if y2 - y1 == 1 or y2 - y1 == -1:
                if getColor(x2, y2) == getColor(x1, y1):
                    ok = 1
            else:
                ok = 1
        else:
            ok = 1
    if ok == 1:
        return False
    return True

def checkValidBlackPawnMove(x1, y1, x2, y2):
    ok = 0

    if y1 == y2:
        if x1 == 1:
            if x2 != 2 and x2 != 3:
                ok = 1
            if board[x2][y2] != 0:
                ok = 1
            if x2 == 3 and board[2][y2] != 0:
                ok = 1
        else:
            if x2 - x1 != 1:
                ok = 1
            if board[x2][y2] != 0:
                ok = 1
    else:
        if x2 - x1 == 1:
            if y2 - y1 == 1 or y2 - y1 == -1:
                if getColor(x2, y2) == getColor(x1, y1):
                    ok = 1
            else:
                ok = 1
        else:
            ok = 1
    if ok == 1:
        return False
    return True


def checkValidKingMove(x1, y1, x2, y2):

    if abs(x2 - x1) > 1 or abs(y2 - y1) > 1:
        return False
    if x1 == x2 and y1 == y2:
        return False
    if getColor(x2, y2) == getColor(x1, y1):
        return False
    return True


def checkValidKnightMove(x1, y1, x2, y2):

    if getColor(x2, y2) == getColor(x1, y1):
        return False
    elif abs(x2 - x1) == 1 and abs(y2 - y1) == 2:
        return True
    elif abs(x2 - x1) == 2 and abs(y2 - y1) == 1:
        return True
    else:
        return False


def checkValidBishopMove(x1, y1, x2, y2):

    if abs(x2 - x1) == abs(y2 - y1):
        if getColor(x2, y2) != getColor(x1, y1):
            if x2 < x1 and y2 > y1: #up - right
                for i in range(1, abs(x2 - x1)):
                    if getColor(x1 - i, y1 + i) != -1:
                        return False
                return True
            elif x2 < x1 and y2 < y1: #up - left
                for i in range(1, abs(x2 - x1)):
                    if getColor(x1 - i, y1 - i) != -1:
                        return False
                return True
            elif x2 > x1 and y2 > y1: #down - right
                for i in range(1, abs(x2 - x1)):
                    if getColor(x1 + i, y1 + i) != -1:
                        return False
                return True
            elif x2 > x1 and y2 < y1: #down - left
                for i in range(1, abs(x2 - x1)):
                    if getColor(x1 + i, y1 - i) != -1:
                        return False
                return True
        else:
            return False
    else:
        return False

def checkValidRookMove(x1, y1, x2, y2):


    if getColor(x2, y2) != getColor(x1, y1):
        if x1 == x2:
            for i in range(1, abs(y2 - y1)):
                if y2 > y1:         #right
                    if getColor(x1, y1 + i) != -1:
                        return False
                else:               #left
                    if getColor(x1, y1 - i) != -1:
                        return False
            return True
        elif y1 == y2:
            for i in range(1, abs(x2 - x1)):
                if x2 > x1:         #up
                    if getColor(x1 - i, y1) != -1:
                        return False
                else:               #down
                    if getColor(x1 - i, y1) != -1:
                        return False
            return True
        else:
            return False
    else:
        return False

def checkValidQueenMove(x1, y1, x2, y2):
    if checkValidRookMove(x1, y1, x2, y2) or checkValidBishopMove(x1, y1, x2, y2):
        return True
    return False




def getCoords(piece):
    for i in range(8):
        for j in range(8):
            if board[i][j] == piece:
                return [i,j]


def isCheckWhite():
    global whiteToMove
    kx, ky = getCoords('Kw')

    for i in range(8):
        for j in range(8):
            if canMove(i, j, kx, ky):
                return True

    return False

def isCheckBlack():
    global whiteToMove
    kx, ky = getCoords('Kb')

    for i in range(8):
        for j in range(8):
            if canMove(i, j, kx, ky):
                return True

    return False



## TODO save move
def safeMove(x, y):
    if protected(x, y) == True:
        return False
    return True


def canMove(x1,y1,x2,y2):
    ok = True

    if board[x1][y1] == 0:
        return False

    global whiteToMove
    ok = ok and (whiteToMove == (board[x1][y1][1] == 'w'))

    if board[x1][y1] == 'Pw':
        ok = ok and checkValidWhitePawnMove(x1, y1, x2, y2)
    if board[x1][y1] == 'Pb':
        ok = ok and checkValidBlackPawnMove(x1, y1, x2, y2)
    if board[x1][y1] == 'Kw' or board[x1][y1] == 'Kb':
        ok = ok and checkValidKingMove(x1, y1, x2, y2)
    if board[x1][y1] == 'Nw' or board[x1][y1] == 'Nb':
        ok = ok and checkValidKnightMove(x1, y1, x2, y2)
    if board[x1][y1] == 'Bw' or board[x1][y1] == 'Bb':
        ok = ok and checkValidBishopMove(x1, y1, x2, y2)
    if board[x1][y1] == 'Rw' or board[x1][y1] == 'Rb':
        ok = ok and checkValidRookMove(x1, y1, x2, y2)
    if board[x1][y1] == 'Qw' or board[x1][y1] == 'Qb':
        ok = ok and checkValidQueenMove(x1, y1, x2, y2)

    return ok

def movePiece(init, final):

    y1 = ord(init[0]) - ord('A')
    x1 = ord(init[1]) - ord('1')
    y2 = ord(final[0]) - ord('A')
    x2 = ord(final[1]) - ord('1')

    x1 = 7 - x1
    x2 = 7 - x2


    if not canMove(x1,y1,x2,y2):
        print("Invalid Move")
        return
    global whiteToMove
    boardCopy = deepcopy(board)

    board[x2][y2] = board[x1][y1]
    board[x1][y1] = 0
    movesStack.append(boardCopy)
    whiteToMove = not whiteToMove

    if not whiteToMove:
        if isCheckWhite():
            undo()
            print('Invalid Move')
            return
    else:
        if isCheckBlack():
            undo()
            print('Invalid move')
            return






def undo():
    boardCopy = movesStack.pop()
    global board
    board = deepcopy(boardCopy)
    global whiteToMove
    whiteToMove = not whiteToMove


def getLetter(keys):
    if keys[pygame.K_a]:
        return 'A'
    if keys[pygame.K_b]:
        return 'B'
    if keys[pygame.K_c]:
        return 'C'
    if keys[pygame.K_d]:
        return 'D'
    if keys[pygame.K_e]:
        return 'E'
    if keys[pygame.K_f]:
        return 'F'
    if keys[pygame.K_g]:
        return 'G'
    if keys[pygame.K_h]:
        return 'H'
    return ''

def getDigit(keys):
    if keys[pygame.K_1]:
        return '1'
    if keys[pygame.K_2]:
        return '2'
    if keys[pygame.K_3]:
        return '3'
    if keys[pygame.K_4]:
        return '4'
    if keys[pygame.K_5]:
        return '5'
    if keys[pygame.K_6]:
        return '6'
    if keys[pygame.K_7]:
        return '7'
    if keys[pygame.K_8]:
        return '8'
    return ''

# init

board = [ ['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb'], #8
          ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'], #7
          [  0,    0,    0,    0,    0,    0,    0,    0],  #6
          [  0,    0,    0,    0,    0,    0,    0,    0],  #5
          [  0,    0,    0,    0,    0,    0,    0,    0],  #4
          [  0,    0,    0,    0,    0,    0,    0,    0],  #3
          ['Pw', 'Pw', 'Pw',  'Pw', 'Pw', 'Pw', 'Pw', 'Pw'], #2
          ['Rw', 'Nw', 'Bw',  'Qw', 'Kw', 'Bw', 'Nw', 'Rw'] ]#1
          # a      b     c     d     e     f     g     h

# init gui
pygame.init()
screen = pygame.display.set_mode((600,600))

background1 = pygame.image.load(os.path.join('Media','board1.png')).convert()
background2 = pygame.image.load(os.path.join('Media','board2.png')).convert()
pieces_image = pygame.image.load(os.path.join('Media','Chess_Pieces_Sprite.png')).convert_alpha()

size_of_bg = background1.get_rect().size
square_width = int(size_of_bg[0] / 8)
square_height = int(size_of_bg[1] / 8)

pieces_image = pygame.transform.scale(pieces_image,
                                  (square_width * 6, square_height * 2))

screen = pygame.display.set_mode(size_of_bg)


gameOver = False
move = ''
nextIsLetter = True
showTable = True
lastChange = 0
boardWithHelp = True
whiteToMove = True
movesStack = []

drawBoard()
pygame.display.update()


# MAIN LOOP
while not gameOver:
    pygame.time.delay(10)
    lastChange += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    keys = pygame.key.get_pressed()

# cancel current input
    if keys[pygame.K_x]:
        move = ''
        nextIsLetter = True

# show/hide boardHelp
    if keys[pygame.K_v] and lastChange > 50:
        move = ''
        boardWithHelp = not boardWithHelp
        lastChange = 0

# show/ hide table
    if keys[pygame.K_z] and lastChange > 50:
        move = ''
        showTable = not showTable
        lastChange = 0

#undo
    if keys[pygame.K_u] and lastChange > 30:
        move = ''
        undo()
        lastChange = 0

# get input
    if nextIsLetter:
        x = getLetter(keys)
        if x != '':
            move += x
            nextIsLetter = False
    else:
        x = getDigit(keys)
        if x != '':
            move += x
            nextIsLetter = True

# check complete move
    if len(move) == 4:
        print(move)
        movePiece(move[0:2], move[2:4])
        move = ''


    drawBoard()
    pygame.display.update()


pygame.quit()

