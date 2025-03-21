import os
import json
from moviepy import *
from src.utils.logger import log_info, log_error

class VideoProcessor:
    def __init__(self, output_file="output/final_video.mp4"):
        self.output_file = output_file

    def merge_videos(self, video_data):
        filtered_videos = self._filter_blocked_videos(video_data)
        local_files = self._download_videos(filtered_videos)
        if local_files:
            self._combine_videos(local_files)

    def _filter_blocked_videos(self, video_data):
        if not os.path.exists("blocked_users.json"):
            return video_data

        with open("blocked_users.json", "r") as f:
            blocked_users = json.load(f).get("blocked", [])

        return [video for video in video_data if video["broadcaster_id"] not in blocked_users]

    def _download_videos(self, video_data):
        local_files = []
        os.makedirs("clips", exist_ok=True)

        for idx, video in enumerate(video_data):
            url = video["url"]
            output_name = f"clips/clip_{idx}.mp4"
            log_info(f"Downloading: {url}")
            os.system(f"yt-dlp {url} -o {output_name}")  # Downloads clip
            if os.path.exists(output_name):
                local_files.append(output_name)
        
        return local_files

    def _combine_videos(self, file_list):
        clips = [VideoFileClip(file) for file in file_list]
        final_clip = concatenate_videoclips(clips)
        log_info("Merging clips using MoviePy...")
        final_clip.write_videofile(self.output_file, codec="libx264", audio_codec="aac")
        log_info(f"Final video saved as {self.output_file}")
