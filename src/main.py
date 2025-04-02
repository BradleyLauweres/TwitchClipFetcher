from src.utils.input_handler import UserInputHandler
from src.downloader.clip_fetcher import ClipFetcher
from src.downloader.video_processor import VideoProcessor



class AppController:
    def __init__(self):
        self.clip_fetcher = ClipFetcher()
        self.video_processor = VideoProcessor()

    def run(self):
        game_id = 32399
        print("HI TOM IT NOW DELETES THE OLD CLIPS")
        self.video_processor.delete_clips()
        clip_count = UserInputHandler.get_user_input()
        print("Fetching clips...")
        clips = self.clip_fetcher.get_clips(game_id, clip_count)

        if clips:
            print("Processing videos...")
            self.video_processor.merge_videos(clips)
        else:
            print("No clips found. Exiting.")

if __name__ == "__main__":
    app = AppController()
    app.run()
