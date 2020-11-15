import pygame
import random


pygame.init()

SCREEN_WIDTH = SCREEN_HEIGHT = 400

SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("15 Puzzle")
clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)

def check_validity_of_board(board):
    
    empty_index= board.index(None)
    index_from_bottom = 4 - empty_index // 4
    inversions = 0
    for i in range(len(board) - 1):
        if i == empty_index:
            continue
        number_1 = board[i]
        for j in range(i + 1,len(board)):
            if j == empty_index:
                continue
            number_2 = board[j]
            if number_2 < number_1:
                inversions += 1
    
    print(inversions)
    print(index_from_bottom)
    if index_from_bottom % 2 == 1:
        return not inversions % 2 == 0

    return not inversions % 2 == 1

def generate_board():

    not_valid = True

    board = [None if i == 0 else i for i in range(16)]
    while not_valid:
        random.shuffle(board)

        not_valid = check_validity_of_board(board)
    
    new_board = []
    for i in range(4):
        new_board.append(board[i * 4:i * 4 + 4])
    print(new_board)
    return new_board


board = generate_board()
font = pygame.font.SysFont("comicsansms",42)

winning_board = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,None]]



def check_win():

    return board == winning_board

def create_initial_text_objects():
    
    texts = [[None for _ in range(len(board[0]))] for _ in range(len(board[0]))]
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] != None:
                text =font.render(f"{board[row][col]}",True,BLACK)
                texts[row][col] = text



    return texts



texts = create_initial_text_objects()






ROWS = COLS = 4
SQUARE_LENGTH = 100

WHITE = (255,255,255)
BLACK = (0,0,0)


surface = pygame.Surface((SQUARE_LENGTH,SQUARE_LENGTH),pygame.SRCALPHA)

WHITE_TRANSPARENT = (0,0,0,50)
surface.fill(WHITE_TRANSPARENT)

def draw_board():

    for y in range(0,SCREEN_HEIGHT,SQUARE_LENGTH):
        pygame.draw.line(SCREEN,BLACK,(0,y),(SCREEN_WIDTH,y))


    for x in range(0,SCREEN_WIDTH,SQUARE_LENGTH):
        pygame.draw.line(SCREEN,BLACK,(x,0),(x,SCREEN_HEIGHT))

    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] != None:
                x,y = col * SQUARE_LENGTH,row * SQUARE_LENGTH
                text = texts[row][col] 
                SCREEN.blit(text,(x + (SQUARE_LENGTH//2 - text.get_width()//2),y + SQUARE_LENGTH//2 - text.get_height()//2))
            else:
                pygame.draw.rect(SCREEN,BLACK,(col * SQUARE_LENGTH,row * SQUARE_LENGTH,SQUARE_LENGTH,SQUARE_LENGTH))

def display_animation(row,col,neighbor_row,neighbor_col):
    
    previous = board[row][col]
    board[row][col] = None
    square = pygame.Surface((SQUARE_LENGTH,SQUARE_LENGTH))
    square.fill(WHITE)
    
    vertical = False
    if neighbor_row != row:
        vertical = True
        current = row * SQUARE_LENGTH
        target = neighbor_row * SQUARE_LENGTH
        delta = -1 if neighbor_row < row else 1
    else:
        current = col * SQUARE_LENGTH
        target = neighbor_col * SQUARE_LENGTH
        delta = -1 if neighbor_col < col else 1
    

    number_text = font.render(str(previous),True,(0,0,0))
    
    while current != target:
        current += delta
        SCREEN.fill(WHITE)
        draw_board()
        SCREEN.blit(square,(current if not vertical else col * SQUARE_LENGTH,current if vertical else row * SQUARE_LENGTH))
        if vertical:
            text_coordinates = (col * SQUARE_LENGTH + (SQUARE_LENGTH//2 - number_text.get_width()//2),current + (SQUARE_LENGTH//2 -number_text.get_height()//2))
        else:
            text_coordinates = (current + (SQUARE_LENGTH//2 - number_text.get_width()//2),row * SQUARE_LENGTH + (SQUARE_LENGTH//2 - number_text.get_height()//2))
        SCREEN.blit(number_text,text_coordinates)
        pygame.display.update()


    board[row][col] = previous









def if_valid_square_switch(row,col):

    for neighbor_row,neighbor_col in ((row + 1,col),(row -1,col),(row,col + 1),(row,col -1)):

        if 0 <= neighbor_row < ROWS and 0 <= neighbor_col < COLS and board[neighbor_row][neighbor_col] == None:

            display_animation(row,col,neighbor_row,neighbor_col)
            board[row][col],board[neighbor_row][neighbor_col] = board[neighbor_row][neighbor_col],board[row][col]
            texts[row][col],texts[neighbor_row][neighbor_col] = texts[neighbor_row][neighbor_col],texts[row][col]
            return True
            

    return False



done = False

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            col,row = x//SQUARE_LENGTH,y//SQUARE_LENGTH
            valid = if_valid_square_switch(row,col)
            if valid:
                game_over = check_win() 
                #generate a new board
            



    SCREEN.fill(WHITE)
    draw_board()
    if pygame.mouse.get_focused() == 1:
        x,y = pygame.mouse.get_pos()
        col,row = x//SQUARE_LENGTH,y//SQUARE_LENGTH
        SCREEN.blit(surface,(col * SQUARE_LENGTH,row * SQUARE_LENGTH))



    pygame.display.update()







