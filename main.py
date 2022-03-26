import numpy as np
import random
import pygame
import math
import sys

#
#   INICIALITZACIO DE VARIABLES
#
BLACK = (0,0,0)      # Defincio del color negre
GREY = (120,120,120) # Defincio del color gris
RED = (255,0,0)      # Defincio del color vermell
YELLOW = (255,255,0) # Defincio del color groc
GREEN = (0,128,0)    # Defincio del color verd
WHITE = (255,255,255)# Defincio del color blanc
BLUE = (0,0,255)     # Defincio del color blanc

ROW_COUNT = 6        # Numero de files del tauler
COLUMN_COUNT = 8     # Numero de columnes del tauler

PLAYER = 0           # Codi del jugador huma
AI = 1               # Codi del jugador AI

EMPTY = 0            # Codi de posicio lliure
PLAYER_PIECE = 1     # Codi de posicio jugador huma
PLAYER_PAINTED = 3   # Codi de posicio pintada per huma

AI_PIECE = 2         # Codi de posicio jugador AI
AI_PAINTED = 4       # Codi de posicio pintada per AI 
WINNER_PIECE = 5     # Codi de posicio guanyadora
BURNED = 6           # Codi de posicio cremada no jugable

#DEPH_LEVEL = ROW_COUNT * COLUMN_COUNT # Limit de profunditat de l'arbre
DEPH_LEVEL = 1   # Profunditat de l'arbre base

#
# DEFINICIO DE MODULS
#

def crear_tauler(): # Crea la matriu de mida files per columnes, que utilitzarem per identificar els estats
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def moure_fitxa(board, row, col, piece):  # Segons l estat i el moviment, replanteja el seguent estat
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == piece: # Segons la fitxa moguda, s'assigna valor al tauler
                if piece == PLAYER_PIECE:
                    board[r][c] = PLAYER_PAINTED
                elif piece == PLAYER_PAINTED:
                    board[r][c] = PLAYER_PIECE
                elif piece == AI_PIECE:
                    board[r][c] = AI_PAINTED
                elif piece == AI_PAINTED:
                    board[r][c] = AI_PIECE
    board[row][col] = piece

def es_posicio_valida(board, row, col, player): # Avalua, segons l estat, si el moviment del jugador indicat compleix les restriccions (NO cal que estigui lliure)
    valid = 0
    if (board[row][col] != EMPTY): # Posicio ocupada pel propi jugador, o pel contrari
        valid = 0
    elif ((row < ROW_COUNT-1) and (board[row+1][col] == player)) or ((row > 0) and (board[row-1][col] == player)): # Jugador en la mateixa columna, fila anterior o posterior
        valid = 1
    elif ((col < COLUMN_COUNT-1) and (board[row][col+1] == player)) or ((col > 0) and (board[row][col-1] == player)): # Jugador en la mateixa fila, columna anterior o posterior
        valid = 1
    return valid

def mostra_tauler(board): # Mostra el tauler per consola
    print(np.flip(board, 0))

def jugada_guanyadora(board, player): # Avalua algunes de les condiciona d'aturada
    winning = False
    painted = 0
    pair = False

    for c in range(COLUMN_COUNT): # Compta fitxes de cada jugador, de forma separada
        for r in range(ROW_COUNT):
            if  (player == PLAYER_PIECE) and (board[r][c] == PLAYER_PAINTED):
                painted+=1
            elif (player == AI_PIECE) and (board[r][c] == AI_PAINTED):
                painted+=1

    if (COLUMN_COUNT*COLUMN_COUNT) % 2 == 0: # Cal tenir en compte si el num de posicions es parell o imparell per calcular si posicio guanyadora (+1 o no)
        pair = True

    if (painted >= (COLUMN_COUNT*ROW_COUNT)/2 and not pair) or (painted == ((COLUMN_COUNT*ROW_COUNT)/2)-1 and pair): # Si comptador de pintades igual o major a la meitat de les posicions
        winning = True  # Verifica posicio guanyadora

    if  (player == PLAYER_PIECE): # Si l'altre jugador esta ofegat guanya jugador contrari
        if len(recupera_posicions_valides(board, AI_PIECE)) == 0:
            winning = True
    elif len(recupera_posicions_valides(board, PLAYER_PIECE)) == 0:
            winning = True

    return winning

def es_node_terminal(board):
    return jugada_guanyadora(board, PLAYER_PIECE) or jugada_guanyadora(board, AI_PIECE) or len(recupera_posicions_valides(board, PLAYER_PIECE)) == 0 or len(recupera_posicions_valides(board, AI_PIECE)) == 0

def recupera_posicions_valides(board, player):
    posicions_valides = []
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            if es_posicio_valida(board, row, col, player):
                posicions_valides.append([ROW_COUNT-row-1,col])
    return posicions_valides

def avalua_estat(board, piece):
    # Cal reprogramar aquest modul, per avaluar cada estat.
    # Us deixo un funcio d exemple, pero l'heu de modificar/millorar.
    # Donat que l'avaluacio de qualsevol tauler, ara es zero (tot i tenir avantatge)
    score = Pplayer = Aplayer = 0
    return score # Retorna puntuacio de l'estat

def minimax(board, depth, alpha, beta, maximizingPlayer):
    # Cal reprogramar aquest modul, per avaluar cada estat.
    # Us deixo un funcio d exemple, pero l'heu de modificar/millorar
    # Utilitza crides recursives fins jugada_guanyadora, o no posicions lliures
    # Retorna l'avaluacio (MAX o MIN) segons jugador, o avaluacio segons heuristica
    if maximizingPlayer:
        posicions_valides = recupera_posicions_valides(board, AI_PIECE)
    else:
        posicions_valides = recupera_posicions_valides(board, PLAYER_PIECE)

    es_terminal = es_node_terminal(board) # Comprova si hi ha alguna jugada no guanyadora possible
    if depth == 0 or es_terminal: # La profunditat es decreixent, comenca a #DEPTH i resta un nivell fins a zero
        if es_terminal: 
            if jugada_guanyadora(board, AI_PIECE):
                return (None, None, 0)
            elif jugada_guanyadora(board, PLAYER_PIECE):
                return (None, None, 0)
            else: # Joc acabat, no hi ha mes moviments valids pendents (taules)
                return (None,None, 0)
        else: # Maxim nivell de produnditat, no terminal
            if maximizingPlayer:
                new_score = avalua_estat(board, AI_PIECE)
            else:
                new_score = avalua_estat(board, PLAYER_PIECE)
            return (None, None, new_score)
    
    if maximizingPlayer:
        value = float('-inf')
        position = random.choice(posicions_valides) # Trio una posicio a l'atzar com a inicialitzacio
        for pos in posicions_valides: # Recorro totes les posicions valides
            b_copy = board.copy()     # Preparo nou tauler        
            
            moure_fitxa(b_copy, ROW_COUNT-pos[0]-1, pos[1], AI_PIECE)   # Mou a nova posicio valida, dins del nou tauler
            temp = minimax(b_copy, depth-1, alpha, beta, False)
            new_score = temp[2]
            if new_score > value:
                value = new_score
                position = pos
            
        return position[0], position[1], value
    else:
        value = float('inf')
        position = random.choice(posicions_valides) # Trio una posicio valida com inicialitzacio
        for pos in posicions_valides:
            b_copy = board.copy()        

            moure_fitxa(b_copy, ROW_COUNT-pos[0]-1, pos[1], PLAYER_PIECE)
            temp = minimax(b_copy, depth-1, alpha, beta, True) # Recupera nomes valor minimax
            new_score = temp[2]
            if new_score < value:
                value = new_score
                position = pos
    
        return position[0], position[1], value

def dibuixa_tauler(board): # Dibuixa tauler via GUI
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, WHITE, (c*SQUARESIZE, r*SQUARESIZE, SQUARESIZE-2, SQUARESIZE),1) # Superposem la graella en blanc 
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):		
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS,2)
            elif board[r][c] == AI_PIECE: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS,2)
            elif board[r][c] == PLAYER_PAINTED: 
                pygame.draw.rect(screen, RED, (c*SQUARESIZE, height-(r*SQUARESIZE)-SQUARESIZE, SQUARESIZE-2, SQUARESIZE-2))
            elif board[r][c] == AI_PAINTED: 
                pygame.draw.rect(screen, YELLOW, (c*SQUARESIZE, height-(r*SQUARESIZE)-SQUARESIZE, SQUARESIZE-2, SQUARESIZE-2))
            elif board[r][c] == WINNER_PIECE: 
                pygame.draw.circle(screen, GREEN, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == BURNED: 
                pygame.draw.rect(screen, GREY, (c*SQUARESIZE, height-(r*SQUARESIZE)-SQUARESIZE, SQUARESIZE-2, SQUARESIZE-2))
    pygame.display.update()

"""
********************************
*          JOC SPLATOON        *
********************************
"""
board = crear_tauler() # Crea tauler de joc
mostra_tauler(board)
game_over = False

pygame.init()
SQUARESIZE = 100 # Quadrats de 100 pixels quadrats
width = COLUMN_COUNT * SQUARESIZE
height = ROW_COUNT * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5) # Radi fitxa
myfont = pygame.font.SysFont("monospace", 75)

# Cal reprogramar qui gaunya el torn inicial
turn = PLAYER # Obligo a comencar a jugador huma

# Cal reprogramar la situacio inicial de les fitxes
# Les posicions assignades han de ser aleatories i exclussives (poden coincidir en la mateixa posicio)
start = [0,0]
moure_fitxa(board, start[0], start[1], PLAYER_PIECE) # Posiciona fitxa humana
start = [5,5]
moure_fitxa(board, start[0], start[1], AI_PIECE) # Posiciona fitxa IA

screen = pygame.display.set_mode(size)
dibuixa_tauler(board)
pygame.display.update()

while not game_over: # Mentre hi ha partida
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if turn == PLAYER:      # Espera la jugada humana
                posx = event.pos[0] # Recupera la posicio (columna) clicada
                posy = event.pos[1] # Recupera la posicio (fila) clicada

                row = int(math.floor((ROW_COUNT*SQUARESIZE-posy)/SQUARESIZE)) # Cal invertir el calcul d'y!
                col = int(math.floor(posx/SQUARESIZE))
                
                if es_posicio_valida(board, row, col, PLAYER_PIECE):
                    moure_fitxa(board, row, col, PLAYER_PIECE)

                    if jugada_guanyadora(board, PLAYER_PIECE):
                        moure_fitxa(board, row, col, WINNER_PIECE)
                        mostra_tauler(board)
                        dibuixa_tauler(board)
                        
                        label = myfont.render("Guanya huma!", 1, BLUE)
                        screen.blit(label, (40,10))
                        pygame.display.flip()
                        game_over = True
                    else:
                        mostra_tauler(board)
                        dibuixa_tauler(board)
                    turn += 1
                    turn = turn % 2

    if turn == AI and not game_over: # Espera la jugada d'IA
        row, col, minimax_score = minimax(board, DEPH_LEVEL, float('-inf'), float('inf'), True) # Al tanto amb aquest - + infinits!
        pygame.time.wait(500)
        moure_fitxa(board, ROW_COUNT-row-1, col, AI_PIECE)

        if jugada_guanyadora(board, AI_PIECE):
            moure_fitxa(board, ROW_COUNT-row-1, col, WINNER_PIECE)
            mostra_tauler(board)
            dibuixa_tauler(board)

            label = myfont.render("Guanya IA!", 1, BLUE)
            screen.blit(label, (40,10))
            pygame.display.flip()
            game_over = True
        else:
            mostra_tauler(board)
            dibuixa_tauler(board)
        turn += 1
        turn = turn % 2

    if game_over:
        pygame.time.wait(3000)