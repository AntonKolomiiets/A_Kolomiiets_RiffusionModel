# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip

def count_frames(video_path):
    
    video = VideoFileClip(video_path)
    
    frame_count = 0
    for _ in video.iter_frames():
        frame_count += 1
    
    return frame_count


def split_video(video_path, num_clips):
    # Load the video
    video = VideoFileClip(video_path)
    
    # Get video properties
    fps = video.fps
    duration = video.duration
    total_frames = count_frames(video_path)  # Total number of frames

    # Calculate the duration for each clip
    clip_frames = total_frames // num_clips  # Number of frames per clip
    clip_duration = clip_frames / fps  # Duration of each clip based on frames
    # last_clip_frames = total_frames - (clip_frames * (num_clips - 1))  

    clips = []
    for i in range(num_clips):
        start_time = i * clip_duration
        if i == num_clips - 1:
            end_time = duration  # Ensure last clip goes till the end
        else:
            end_time = start_time + clip_duration
        
        # Save each clip
        clip_path = f"clip_{i}.mp4"
        # video.subclip(start_time, end_time).write_videofile(clip_path, codec='libx264', audio_codec='aac')
        subclip = video.subclip(start_time, end_time)
        subclip.write_videofile(clip_path, codec='libx264', audio_codec='aac')

        clips.append(clip_path)
    
    return clips
