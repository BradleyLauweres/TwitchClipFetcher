import os
import subprocess
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
            os.system(f"yt-dlp {url} -o {output_name}") 
            if os.path.exists(output_name):
                local_files.append(output_name)
        
        return local_files

    def _combine_videos(self, file_list):
    
        reencoded_files = self._reencode_clips(file_list)

        clips_dir = "clips"
        file_list_path = os.path.join(clips_dir, "file_list.txt")

 
        with open(file_list_path, "w") as f:
            for file in reencoded_files:
                file_relative = os.path.basename(file)
                f.write(f"file '{file_relative}'\n")

        log_info("Merging clips using FFmpeg...")

 
        subprocess.run([
         "ffmpeg", 
            "-f", "concat", 
            "-safe", "0", 
            "-i", file_list_path,
            "-c:v", "libx264",  # Re-encode to H.264 video codec
            "-c:a", "aac",      # Re-encode audio to AAC codec
            "-strict", "experimental",  # Ensure AAC support
            "-preset", "fast",  # Faster encoding preset
            "-crf", "23",       # Constant rate factor for quality control
            "-y",               # Overwrite the output file if it exists
            self.output_file
    ])

        log_info(f"Final video saved as {self.output_file}")

    def _reencode_clips(self, file_list):
        reencoded_files = []

        for idx, file in enumerate(file_list):
            reencoded_file = f"clips/reencoded_clip_{idx}.mp4"
            log_info(f"Re-encoding {file} to {reencoded_file}...")

            subprocess.run([
                "ffmpeg", 
                "-i", file, 
                "-c:v", "libx264",  # Re-encode video
                "-c:a", "aac",      # Re-encode audio
                "-strict", "experimental", 
                "-preset", "fast",  # Faster encoding preset
                "-crf", "23","-y",  # Constant rate factor for quality control
                reencoded_file
            ])

            reencoded_files.append(reencoded_file)

        return reencoded_files