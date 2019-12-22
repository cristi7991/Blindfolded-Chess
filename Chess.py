import pygame
import os

def getColor(x,y):
    if board[x][y] == 0:
        return -1
    if board[x][y] in {'Rw', 'Nw', 'Bw', 'Kw', 'Qw', 'Pw'}:
        return 0;
    return 1

def getPieceImage(x):

    if x == 'Kw':
        return [0,0]
    if x == 'Qw':
        return [square_width, 0]
    if x == 'Bw':
        return [2*square_width, 0]
    if x == 'Nw':
        return [3*square_width, 0]
    if x == 'Rw':
        return [4*square_width, 0]
    if x == 'Pw':
        return [5*square_width, 0]

    if x == 'Kb':
        return [0,square_height]
    if x == 'Qb':
        return [square_width, square_height]
    if x == 'Bb':
        return [2*square_width, square_height]
    if x == 'Nb':
        return [3*square_width, square_height]
    if x == 'Rb':
        return [4*square_width, square_height]
    if x == 'Pb':
        return [5*square_width, square_height]



def drawBoard():
    #Blit the background:
    if boardWithHelp:
        screen.blit(background1,(0,0))
    else:
        screen.blit(background2, (0, 0))
    if showTable:
        for i in range(8):
            for j in range(8):
                if board[i][j] != 0:
                    [x,y] = getPieceImage(board[i][j])
                    screen.blit(pieces_image, (j*square_width,i*square_height), (x,y,square_width,square_height))

def checkValidWhitePawnMove(x1,y1,x2,y2):

    ok = 0
    print(x1, y1, x2, y2)
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

                if getColor(x2, y2) != getColor(x1, y1):
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

    print(x1,y1,x2,y2)
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
                if getColor(x2, y2) != getColor(x1, y1):
                    ok = 1
            else:
                ok = 1
        else:
            ok = 1
    if ok == 1:
        return False
    return True


def movePiece(init, final):

    ok = True
    y1 = ord(init[0]) - ord('A')
    x1 = ord(init[1]) - ord('1')
    y2 = ord(final[0]) - ord('A')
    x2 = ord(final[1]) - ord('1')

    x1 = 7-x1
    x2 = 7-x2
    if board[x1][y1] == 0:
        print('Invalid move')
        return

    if board[x1][y1] == 'Pw':
        ok = ok and checkValidWhitePawnMove(x1,y1,x2,y2)
    if board[x1][y1] == 'Pb':
        ok = ok and checkValidBlackPawnMove(x1, y1, x2, y2)


    if not ok:
        print('Invalid move')
        return
    board[x2][y2] = board[x1][y1]
    board[x1][y1] = 0

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
square_width = int(size_of_bg[0]/8)
square_height = int(size_of_bg[1]/8)

pieces_image = pygame.transform.scale(pieces_image,
                                      (square_width*6,square_height*2))

screen = pygame.display.set_mode(size_of_bg)



gameOver = False
move = ''
nextIsLetter = True
showTable = True
lastChange = 0
boardWithHelp = True

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






