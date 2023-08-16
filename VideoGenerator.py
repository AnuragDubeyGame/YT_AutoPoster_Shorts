from gtts import gTTS
from mutagen.mp3 import MP3
import numpy as np
import cv2
from moviepy.editor import VideoFileClip, AudioFileClip, clips_array

def create_colored_screen_video(mp3_duration, output_filename, color_rgb, target_aspect_ratio):
    # Define video properties
    fps = 30
    frame_height = 480  # Set a fixed frame height
    frame_width = int(frame_height * target_aspect_ratio)

    total_frames = int(fps * mp3_duration)

    # Create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))

    # Create colored frames and write to the video
    color_bgr = color_rgb[::-1]  # Convert RGB to BGR
    for _ in range(total_frames):
        frame = np.ones((frame_height, frame_width, 3), dtype=np.uint8) * color_bgr
        video_writer.write(frame)

    # Release the video writer
    video_writer.release()

def merge_audio_video(audio_filename, video_filename, output_filename):
    audio_clip = AudioFileClip(audio_filename)
    video_clip = VideoFileClip(video_filename)
    
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_filename, codec="libx264")

fact = "Mars has 80% of Earth's gravity"
tts = gTTS(text=fact, lang="en")

# Save the generated speech as an MP3 file
mp3_filename = "fact.mp3"
tts.save(mp3_filename)

# Get the duration of the generated MP3 file
mp3 = MP3(mp3_filename)
duration = mp3.info.length

# Specify the RGB value for the colored frame (e.g., black)
black_rgb = (25, 245, 225)

# Specify the target aspect ratio (9:16)
target_aspect_ratio = 9 / 16.0

# Create the colored screen video
output_video_filename = "output_video.mp4"
create_colored_screen_video(duration, output_video_filename, black_rgb, target_aspect_ratio)

# Merge the audio and video
output_merged_filename = "merged_video.mp4"
merge_audio_video(mp3_filename, output_video_filename, output_merged_filename)
