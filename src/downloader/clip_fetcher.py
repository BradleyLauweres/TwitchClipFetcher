import requests
from datetime import datetime, timedelta
from src.utils.logger import log_info, log_error

class ClipFetcher:
    BASE_URL = "https://api.twitch.tv/helix/clips"
    BASE_URL_USERS = "https://api.twitch.tv/helix/users"

    def __init__(self):
        self.headers = {
            "Client-ID": "gs44smut15275gf87pqx9v0p9nqpi5",
            "Authorization": f"Bearer ea65d1wb7yw1w5n1pdjbzx84b3g9s8"
        }

    def get_broadcastID(self):
        broadcaster_name = input("Please enter the broadcaster name: ")
        response = requests.get(self.BASE_URL_USERS, headers=self.headers, params={"login": broadcaster_name})
        broadcaster_id = response.json().get("data", [{}])[0].get("id")
        print(broadcaster_id)
        return broadcaster_id

    def get_clips(self, game_id, clip_count):
        now = datetime.now().isoformat() + "Z"
        wantToChangeBaseTime = input("Do you want to change the base time? (y/n): ")

        if wantToChangeBaseTime == "y":
            pickedDate = int(input("Please enter the hours the started_at value should be"))
            twenty_four_hours_ago = (datetime.now() - timedelta(hours=pickedDate)).isoformat() + "Z"
        else:
            twenty_four_hours_ago = (datetime.now() - timedelta(hours=24)).isoformat() + "Z"

        wantToEnterBroadcasterID = input("Do you want to enter a broadcaster ID? (y/n): ")
      
        if wantToEnterBroadcasterID == "y":
            broadcast_id = self.get_broadcastID()
            params = {"started_at": twenty_four_hours_ago, "ended_at": now, "first": clip_count, "broadcaster_id": broadcast_id}
        else:
            params = {"game_id": game_id, "started_at": twenty_four_hours_ago,"ended_at":now, "first": clip_count}
        
        response = requests.get(self.BASE_URL, headers=self.headers, params=params)
        
        if response.status_code != 200:
            log_error(f"Error fetching clips: {response.text}")
            return []
        
        clips = response.json().get("data", [])
        log_info(f"Fetched {len(clips)} clips.")
        
        return [{"url": clip["url"], "broadcaster_id": clip["broadcaster_id"]} for clip in clips]
    
    
