class Explosion:
    def __init__(self, pos_x, pos_y, animation_counter = 0, animation_last_update = -1):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.animation_counter = animation_counter
        self.animation_last_update = animation_last_update