class Enemy_Wave:
    def __init__(self, wave_number, alien_movement_speed, alien_spawn_speed, alien_amount, alien_health, wave_defeated):
        self.wave_number = wave_number
        self.alien_movement_speed = alien_movement_speed
        self.alien_spawn_speed = alien_spawn_speed
        self.alien_amount = alien_amount
        self.alien_health = alien_health
        self.wave_defeated = wave_defeated

def init_enemy_waves():
    enemy_waves = [
    Enemy_Wave(0, 30, 100, 10, 1, False),
    Enemy_Wave(1, 250, 1000, 1, 1, False),
    Enemy_Wave(2, 200, 800, 1, 2, False),
    Enemy_Wave(3, 250, 800, 1, 2, False),
    Enemy_Wave(4, 250, 800, 3, 3, False),
    Enemy_Wave(5, 300, 800, 2, 3, False),
    Enemy_Wave(6, 250, 800, 999999, 3, False)]
    return enemy_waves