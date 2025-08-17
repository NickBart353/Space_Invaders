class Alien:
    def __init__(self, name, pos_x, pos_y, movement_direction, rect = None):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.movement_direction = movement_direction
        self.rect = rect