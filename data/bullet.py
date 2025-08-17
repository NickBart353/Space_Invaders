class Bullet:
    def __init__(self, pos_x, pos_y, last_bullet_movement_update, rect = None):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.last_bullet_movement_update = last_bullet_movement_update
        self.rect = rect