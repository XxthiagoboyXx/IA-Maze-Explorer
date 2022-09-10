import random


class Player:
    def __init__(self, name: str, pos_x: int, pos_y: int):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y

    def randomMove(self, listMove):
        escolha = random.choice(listMove)
        #print(escolha)
        if escolha == 'left':
            self.pos_x -= 1
        elif escolha == 'right':
            self.pos_x += 1
        elif escolha == 'up':
            self.pos_y -= 1
        elif escolha == 'down':
            self.pos_y += 1

        return escolha

    def move(self, cell):
        listMove = [cell.left, cell.right, cell.up, cell.down]
        escolha = listMove.index(max(listMove))

        #print(f"x -> {cell.x} y -> {cell.y}")
        #print(f'reward -> {cell.reward}')
        #print(f'left -> {cell.left} | right -> {cell.right} | up -> {cell.up} | down -> {cell.down} |')

        if escolha == 0:
            self.pos_x -= 1
        elif escolha == 1:
            self.pos_x += 1
        elif escolha == 2:
            self.pos_y -= 1
        elif escolha == 3:
            self.pos_y += 1

        return escolha