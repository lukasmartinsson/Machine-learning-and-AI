class Move:
    def __init__(self, player, x, y):
        self.player = player
        self.x = x
        self.y = y

    def __repr__(self):
        return "Move()"

    def __str__(self):
        return f"[{self.x}, {self.y}]"
