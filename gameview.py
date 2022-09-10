import pygame
from cell import *
from map import *
import time
import pickle
import base64

MAP_FREE = 0
MAP_WALL = 1
MAP_PLAYER = 2
MAP_OBJETIVE = 3

game_map = []
map_number = 0

def choice_map(map_choice):

    global game_map
    global map_number

    if map_choice == 1:
        game_map = map_1
    elif map_choice == 2:
        game_map = map_2
    elif map_choice == 3:
        game_map = map_3
    elif map_choice == 4:
        game_map = map_4
    elif map_choice == 5:
        game_map = map_5

    map_number = map_choice
    return  game_map




COLOR_GREY = (46, 46, 46)
COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (0, 200, 255)
COLOR_DARK_GREY = (169, 160, 181)
COLOR_GREEN = (144, 238, 144)
COLOR_RED = (255, 69, 0)
COLOR_BLACK = (0, 0, 0)


#PIXEL_SIZE = 30
PIXEL_SIZE = 15

WIDTH_POSITION = len(game_map) * PIXEL_SIZE
HEIGHT_POSITION = len(game_map) * PIXEL_SIZE

pygame.init()
screen = pygame.display.set_mode((WIDTH_POSITION, HEIGHT_POSITION))
pygame.display.set_caption('IA Discover')
clock = pygame.time.Clock()
screen.fill(COLOR_GREY)

CONST_ALGORITMO = 0.8

def draw(x, y, color):
    pygame.draw.rect(screen, color, (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))


def first_render_screen():
    for y in range(0, len(game_map)):
        for x in range(0, len(game_map)):
            pos_x = x * PIXEL_SIZE
            pos_y = y * PIXEL_SIZE
            if game_map[y][x] == MAP_PLAYER:
                pygame.draw.rect(screen, COLOR_BLUE,
                                 (pos_x, pos_y, PIXEL_SIZE, PIXEL_SIZE))
            elif game_map[y][x] == MAP_OBJETIVE:
                pygame.draw.rect(screen, COLOR_RED,
                             (pos_x, pos_y, PIXEL_SIZE, PIXEL_SIZE))
            elif game_map[y][x] == MAP_WALL:
                pygame.draw.rect(screen, COLOR_GREY,
                                 (pos_x, pos_y, PIXEL_SIZE, PIXEL_SIZE))
            elif game_map[y][x] == MAP_FREE:
                pygame.draw.rect(screen, COLOR_WHITE,
                                 (pos_x, pos_y, PIXEL_SIZE, PIXEL_SIZE))
            pygame.display.update()


def player_move_event_draw(x_to, y_to, x_from, y_from):
    game_map[y_to][x_to] = MAP_PLAYER
    draw(x_to, y_to, COLOR_BLUE)
    game_map[y_from][x_from] = MAP_FREE
    draw(x_from, y_from, COLOR_WHITE)


def game_exploration(player):
    first_render_screen()

    cellList = []

    for y in range(len(game_map)):
        for x in range(len(game_map)):
            if game_map[y][x] == MAP_FREE or game_map[y][x] == MAP_PLAYER:
                cellList.append(Cell(y, x, 0, 0, 0, 0, 0))
            if game_map[y][x] == MAP_OBJETIVE:
                cellList.append(Cell(y, x, 10, 0, 0, 0, 0))

    for cell in cellList:
        print(cell.x, cell.y, cell.reward)

    allViseted = False
    running = True
    cont = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


        listMove = []
        if player.pos_x - 1 >= 0 and game_map[player.pos_y][player.pos_x - 1] != MAP_WALL:
            listMove.append('left')
        if player.pos_x + 1 < len(game_map) and game_map[player.pos_y][player.pos_x + 1] != MAP_WALL:
            listMove.append('right')
        if player.pos_y - 1 >= 0 and game_map[player.pos_y - 1][player.pos_x] != MAP_WALL:
            listMove.append('up')
        if player.pos_y + 1 < len(game_map) and game_map[player.pos_y + 1][player.pos_x] != MAP_WALL:
            listMove.append('down')

        #logica recompensa
        for cell in cellList:
            if player.pos_x == cell.y and player.pos_y == cell.x:
                cellAnt = cell

        temp_x = player.pos_x
        temp_y = player.pos_y

        move = player.randomMove(listMove)
        player_move_event_draw(player.pos_x, player.pos_y, temp_x, temp_y)

        for cell in cellList:
            if player.pos_x == cell.y and player.pos_y == cell.x:
                cellAtual = cell


        if move == 'left':
            cellAnt.left = cellAtual.reward + CONST_ALGORITMO * max(cellAtual.left, cellAtual.right, cellAtual.up,
                                                                    cellAtual.down)
            print("Peso left ", cellAnt.left)

        elif move == 'right':
            cellAnt.right = cellAtual.reward + CONST_ALGORITMO * max(cellAtual.left, cellAtual.right, cellAtual.up,
                                                                     cellAtual.down)
            print("Peso right ", cellAnt.right)

        elif move == 'up':
            cellAnt.up = cellAtual.reward + CONST_ALGORITMO * max(cellAtual.left, cellAtual.right, cellAtual.up,
                                                                  cellAtual.down)
            print("Peso up ", cellAnt.up)

        elif move == 'down':
            cellAnt.down = cellAtual.reward + CONST_ALGORITMO * max(cellAtual.left, cellAtual.right, cellAtual.up,
                                                                    cellAtual.down)
            print("Peso down ", cellAnt.down)


        pygame.display.update()

        if cont % 5000 == 0:
            numVisiteds = 0
            for cell in cellList:
                if (cell.left, cell.right, cell.up, cell.down).count(0) <= 3:
                    numVisiteds += 1

            if numVisiteds == len(cellList):
                allViseted = True

        if allViseted:
            numCell = 0
            cellSavedList = []
            print(50 * '-')
            for cell in cellList:
                print(f"----cell {numCell}")
                print(f"x -> {cell.x} y -> {cell.y}")
                print(f'reward -> {cell.reward}')
                print(f'left -> {cell.left} | right -> {cell.right} | up -> {cell.up} | down -> {cell.down} |')
                print(f'data saved-> {base64.b64encode(pickle.dumps(cell))}')
                cellSavedList.append(base64.b64encode(pickle.dumps(cell)))
                numCell += 1
            print(50 * '-')
            print("Numero de visitas: ", cont)

            with open(f'db_learning_map_{map_number}.ia', 'w') as file:
                for cell in cellSavedList:
                    file.writelines(str(cell)+'\n')
            input()

        cont += 1



def game_explotation(player):
    first_render_screen()

    cellList = []
    try:
        with open(f'db_learning_map_{map_number}.ia', 'r') as file:
            cellEncodedList = file.readlines()
    except:
        print(f'db_learning_map_{map_number}.ia não encontrado')
        print('Talvez o mapa não tenha sido explorado ainda!')
        exit(1)


    for i in range(len(cellEncodedList)):
        cell = cellEncodedList[i].strip()
        cell = cell.split('\'')
        #print(cell)
        cellEncodedList[i] = str(cell[1])

    for cell in cellEncodedList: #instanciando as cell salvas
        cell = base64.b64decode(cell)
        cellList.append(pickle.loads(cell))

    '''
    print(50 * '-')
    numCell = 0
    for cell in cellList:
        print(f"----cell {numCell}")
        print(f"x -> {cell.x} y -> {cell.y}")
        print(f'reward -> {cell.reward}')
        print(f'left -> {cell.left} | right -> {cell.right} | up -> {cell.up} | down -> {cell.down} |')
        print(f'data saved-> {base64.b64encode(pickle.dumps(cell))}')
        numCell += 1
    print(50 * '-')
    '''


    running = True
    while running:
        #executa o algoritmo
        time.sleep(0.1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        listMove = []
        if player.pos_x - 1 >= 0 and game_map[player.pos_y][player.pos_x - 1] != MAP_WALL:
            listMove.append('left')
        if player.pos_x + 1 < len(game_map) and game_map[player.pos_y][player.pos_x + 1] != MAP_WALL:
            listMove.append('right')
        if player.pos_y - 1 >= 0 and game_map[player.pos_y - 1][player.pos_x] != MAP_WALL:
            listMove.append('up')
        if player.pos_y + 1 < len(game_map) and game_map[player.pos_y + 1][player.pos_x] != MAP_WALL:
            listMove.append('down')

        #logica recompensa
        for cell in cellList:
            if player.pos_x == cell.y and player.pos_y == cell.x:
                cellAnt = cell

        temp_x = player.pos_x
        temp_y = player.pos_y

        move = player.move(cellAnt)
        player_move_event_draw(player.pos_x, player.pos_y, temp_x, temp_y)

        for cell in cellList:
            if player.pos_x == cell.y and player.pos_y == cell.x:
                cellAtual = cell


        if move == 'left':
            cellAnt.left = cellAtual.reward + CONST_ALGORITMO * max(cellAtual.left, cellAtual.right, cellAtual.up,
                                                                    cellAtual.down)
            print("Peso left ", cellAnt.left)

        elif move == 'right':
            cellAnt.right = cellAtual.reward + CONST_ALGORITMO * max(cellAtual.left, cellAtual.right, cellAtual.up,
                                                                     cellAtual.down)
            print("Peso right ", cellAnt.right)

        elif move == 'up':
            cellAnt.up = cellAtual.reward + CONST_ALGORITMO * max(cellAtual.left, cellAtual.right, cellAtual.up,
                                                                  cellAtual.down)
            print("Peso up ", cellAnt.up)

        elif move == 'down':
            cellAnt.down = cellAtual.reward + CONST_ALGORITMO * max(cellAtual.left, cellAtual.right, cellAtual.up,
                                                                    cellAtual.down)
            print("Peso down ", cellAnt.down)


        pygame.display.update()

        if cellAtual.reward == 10:
            print("Encontrou")

        while cellAtual.reward == 10:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()



