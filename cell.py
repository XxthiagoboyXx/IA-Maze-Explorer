class Cell():
    def __init__(self, x: int, y: int, reward: int, left: float, right: float, up: float, down: float):
        self.x = x
        self.y = y
        self.reward = reward
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        print("Celula criada")
