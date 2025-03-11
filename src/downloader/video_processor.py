import os
from moviepy import *
from src.utils.logger import log_info, log_error

class VideoProcessor:
    def __init__(self, output_file="output/final_video.mp4"):
        self.output_file = output_file

    def merge_videos(self, video_urls):
        local_files = self._download_videos(video_urls)
        if local_files:
            self._combine_videos(local_files)

    def _download_videos(self, video_urls):
        local_files = []
        os.makedirs("clips", exist_ok=True)

        for idx, url in enumerate(video_urls):
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
