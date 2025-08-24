class Enemy_Wave:
    def __init__(self, wave_number, alien_movement_speed, alien_spawn_speed, alien_amount, alien_health, wave_defeated, difficulty_increase):
        self.wave_number = wave_number
        self.alien_movement_speed = alien_movement_speed
        self.alien_spawn_speed = alien_spawn_speed
        self.alien_amount = alien_amount
        self.alien_health = alien_health
        self.wave_defeated = wave_defeated
        self.difficulty_increase = difficulty_increase

def init_enemy_waves():
    enemy_waves = [
    Enemy_Wave(0, 150, 800, 10, 1, False,10),
    Enemy_Wave(1, 200, 800, 10, 2, False,10),
    Enemy_Wave(2, 200, 800, 15, 2, False,15),
    Enemy_Wave(3, 250, 800, 15, 3, False,15),
    Enemy_Wave(4, 250, 800, 20, 3, False,20),
    Enemy_Wave(5, 200, 800, 999999, 3, False,20)]
    return enemy_waves