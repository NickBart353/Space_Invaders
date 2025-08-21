class Enemy_Wave:
    def __init__(self, wave_number, alien_movement_speed, alien_spawn_speed, alien_amount, alien_health):
        self.wave_number = wave_number
        self.alien_movement_speed = alien_movement_speed
        self.alien_spawn_speed = alien_spawn_speed
        self.alien_amount = alien_amount
        self.alien_health = alien_health

def init_enemy_waves():
    enemy_waves = [
    Enemy_Wave(0, 300, 1000, 20, 1),
    Enemy_Wave(1, 250, 1000, 30, 1),
    Enemy_Wave(2, 200, 800, 30, 1),
    Enemy_Wave(3, 250, 800, 20, 2),
    Enemy_Wave(4, 250, 800, 30, 2),
    Enemy_Wave(5, 300, 800, 20, 3),
    Enemy_Wave(6, 250, 800, 999999, 3)]
    return enemy_waves