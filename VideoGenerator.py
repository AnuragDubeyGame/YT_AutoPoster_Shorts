from gtts import gTTS
from mutagen.mp3 import MP3
import numpy as np
import cv2
import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip, VideoClip, concatenate_videoclips

def get_random_video(base_videos_folder):
    video_files = [f for f in os.listdir(base_videos_folder) if f.lower().endswith(('.mp4', '.avi', '.mkv', '.mov'))]
    if not video_files:
        raise ValueError("No video files found in the base_videos_folder")

    random_video_filename = random.choice(video_files)
    return os.path.join(base_videos_folder, random_video_filename)

def delete_output_video(filename):
    try:
        os.remove(filename)
        print(f"Deleted {filename}")
    except OSError as e:
        print("Error:", e)
        
def create_video_with_background(audio_duration, base_video_path, output_filename):
    audio_clip = AudioFileClip(mp3_filename)
    base_video_clip = VideoFileClip(base_video_path)
    
    # Set the video duration to match the audio duration
    base_video_clip = base_video_clip.subclip(0, audio_duration)

    final_video_clip = base_video_clip.set_audio(audio_clip)
    final_video_clip.write_videofile(output_filename, codec="libx264")



def crop_video_to_audio_duration(input_video_filename, output_video_filename, audio_duration):
    video_clip = VideoFileClip(input_video_filename)
    cropped_video_clip = video_clip.subclip(0, audio_duration)
    cropped_video_clip.write_videofile(output_video_filename, codec="libx264")

if __name__ == "__main__":
    fact = "The average human brain has about 86 billion neurons."
    tts = gTTS(text=fact, lang="en")

    # Save the generated speech as an MP3 file
    mp3_filename = "fact.mp3"
    tts.save(mp3_filename)

    # Get the duration of the generated MP3 file
    mp3 = MP3(mp3_filename)
    audio_duration = mp3.info.length

    # Specify the target aspect ratio (9:16)
    target_aspect_ratio = 9 / 16.0

    # Get a random video from the "BaseVideos" folder
    base_videos_folder = "BaseVideos"
    random_base_video = get_random_video(base_videos_folder)

    # Create the video with background
    output_video_filename = "output_video.mp4"
    create_video_with_background(audio_duration, random_base_video, output_video_filename)

    # Crop the video to match the audio duration
    cropped_output_filename = "cropped_output_video.mp4"
    crop_video_to_audio_duration(output_video_filename, cropped_output_filename, audio_duration)

    # Delete the intermediate output videos
    delete_output_video(output_video_filename)
