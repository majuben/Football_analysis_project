import sys
sys.path.append('../')
from utils import get_center_of_bbox, get_bbox_width, mesure_distance

class PlayerBallAssigner:
    def __init__(self):
        self.max_player_ball_distance = 45
        
    def assign_ball_to_player(self, players, ball_bbox):
        ball_position = get_center_of_bbox(ball_bbox)
        min_distance = 999999
        assigned_player = -1
        
        for player_id, player in players.items():
            player_bbox = player["bbox"]
            distance_left = mesure_distance((player_bbox[0], player_bbox[-1]), ball_position)
            distance_right = mesure_distance((player_bbox[2], player_bbox[-1]), ball_position)
            distance = min(distance_left, distance_right)
            if distance < self.max_player_ball_distance and distance < min_distance:
                min_distance = distance
                assigned_player = player_id
        return assigned_player