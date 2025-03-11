import requests
#from config import CLIENT_ID, ACCESS_TOKEN
from src.utils.logger import log_info, log_error

class ClipFetcher:
    BASE_URL = "https://api.twitch.tv/helix/clips"

    def __init__(self):
        self.headers = {
            "Client-ID": "gs44smut15275gf87pqx9v0p9nqpi5",
            "Authorization": f"Bearer {"7y6j769vrldwkf1h6s1xszpo194flw"}"
        }

    def get_clips(self, game_id, clip_count):
        params = {"game_id": game_id,"started_at":"2025-03-08T12:34:56Z", "first": clip_count}

        print(self.BASE_URL)
        print(self.headers)
        print(params)

        response = requests.get(self.BASE_URL, headers=self.headers, params=params)

        print(response)
        
        if response.status_code != 200:
            log_error(f"Error fetching clips: {response.text}")
            return []

        clips = response.json().get("data", [])
        log_info(f"Fetched {len(clips)} clips.")
        return [clip["url"] for clip in clips]
