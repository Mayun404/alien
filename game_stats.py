# 统计信息
class GameStats:
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        # self.high_score = 0
        with open('high.txt', 'r') as f:
            self.high_score = int(f.read())

    def reset_stats(self):
        with open('last.txt', 'r') as f:
            self.last_score = int(f.read())
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
