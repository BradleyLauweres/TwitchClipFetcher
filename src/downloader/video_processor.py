import os
import glob
import json
from moviepy import *
from src.utils.logger import log_info, log_error

class VideoProcessor:
    def __init__(self, output_file="output/final_video.mp4"):
        self.output_file = output_file

    def delete_clips(self):
        if not os.path.exists("clips"):
            return
        
        for file in os.listdir("clips"):
            file_path = os.path.join("clips", file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def merge_videos(self, video_data):
        filtered_videos = self._filter_blocked_videos(video_data)
        local_files = self._download_videos(filtered_videos)
        if local_files:
            wantsToMerge = input("Do you want to merge the clips? (y/n): ")
            if wantsToMerge == "y":
                local_files_edited = self.get_clip_files()
                self._combine_videos(local_files_edited)
            else:
                log_info("Clips not merged.")

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
            os.system(f"yt-dlp {url} -o {output_name}")
            if os.path.exists(output_name):
                local_files.append(output_name)
                print("Saving videos in:", os.path.abspath(output_name))
        
        return local_files

    def _combine_videos(self, file_list):
        clips = [VideoFileClip(file) for file in file_list]
        final_clip = concatenate_videoclips(clips)
        log_info("Merging clips using MoviePy...")
        final_clip.write_videofile(self.output_file, codec="libx264", audio_codec="aac")
        log_info(f"Final video saved as {self.output_file}")

    def get_clip_files(self):
        clip_dir = "clips"
        if not os.path.exists(clip_dir):
            return []

        clips = sorted(glob.glob(os.path.join(clip_dir, "clip_*.mp4")))
        return clips
