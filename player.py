from compass_directions import CompassDirection

class Player:
    current_phase = 1
    current_turn = False
    num_dam_tokens = 0
    wind_direction = CompassDirection.N
    wind_speed = 0
    orographic = 0
    dam_fill = 0
    row = -1
    col = -1

    def __init__(self, name):
        self.name = name
        self.score = 0