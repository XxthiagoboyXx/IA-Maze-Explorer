from gameview import *
from player import *


if __name__ == '__main__':

    game_map = choice_map(1) #escolher o mapa

    #para trocar a posicção inicial do player basta mudar a posição onde o número "2" se encontra na matriz do mapa no arquivo "map.py"
    PLAYER_POS_Y, PLAYER_POS_X = get_position(game_map, MAP_PLAYER) #retorna a posição do player na matriz mapa

    player = Player("Player", PLAYER_POS_X, PLAYER_POS_Y)

    game_exploration(player) #para aprender
    #game_explotation(player) #para usufruir do que foi aprendido

