from utils import read_video, save_video
from trackers import Tracker 
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
from camera_movement_estimator import CameraMovementEstimator
import cv2 #type: ignore
import numpy as np #type: ignore




def main():
    video_frames = read_video('input_videos/08fd33_4.mp4')
    
    
    
    tracker = Tracker('models/best.pt')
    tracks = tracker.get_object_tracks(video_frames, read_from_stub=True, stub_path='stubs/track_stubs.pkl')
    
    camera_movement_estimator = CameraMovementEstimator(video_frames[0])
    camera_movement_per_frame = camera_movement_estimator.get_camera_movement(video_frames,
                                                                                read_from_stub=True,
                                                                                stub_path='stubs/camera_movement_stubs.pkl')
    
    tracks["ball"] = tracker.interpolate_ball_positions(tracks["ball"])

    team_assigner = TeamAssigner()  
    team_assigner.assign_team_color(video_frames[0], tracks["players"][0])
    for frame_num, player_track in enumerate(tracks["players"]):
        for player_id, track in player_track.items():
            team = team_assigner.get_player_team(video_frames[frame_num], track["bbox"], player_id)
            tracks["players"][frame_num][player_id]["team"] = team
            tracks["players"][frame_num][player_id]["team_color"] = team_assigner.team_colors[team]
    
    player_assigner = PlayerBallAssigner()
    team_possession = [1]
    for frame_num, player_track in enumerate(tracks["players"]):
        ball_bbox = tracks["ball"][frame_num][1]["bbox"]
        assigned_player = player_assigner.assign_ball_to_player(player_track, ball_bbox)
        
        if assigned_player != -1:
            tracks["players"][frame_num][assigned_player]["has_ball"] = True
            team_possession.append(tracks["players"][frame_num][assigned_player]["team"])
        else:
            team_possession.append(team_possession[-1])
    team_possession = np.array(team_possession)
    
    output_video_frames = tracker.draw_annotations(video_frames, tracks, team_possession)
    
    output_video_frames = camera_movement_estimator.draw_camera_movement(output_video_frames,camera_movement_per_frame)
    
    save_video(output_video_frames, 'output_videos/output_video.avi')
    
if __name__ == "__main__":
    main()