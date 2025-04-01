import requests
from dotenv import load_dotenv,dotenv_values
from datetime import datetime, timedelta
from src.utils.logger import log_info, log_error

class ClipFetcher:
    BASE_URL = "https://api.twitch.tv/helix/clips"
    BASE_URL_USERS = "https://api.twitch.tv/helix/users"

    def __init__(self):
        load_dotenv()
        self.headers = {
            "Client-ID": dotenv_values(".env")["CLIENT_ID"],
            "Authorization": dotenv_values(".env")["ACCESS_TOKEN"],
        }

    def get_broadcastID(self):
        broadcaster_name = input("Please enter the broadcaster name: ")
        response = requests.get(self.BASE_URL_USERS, headers=self.headers, params={"login": broadcaster_name})
        broadcaster_id = response.json().get("data", [{}])[0].get("id")
        print(broadcaster_id)
        return broadcaster_id
    
    def change_base_time(self):
        wantToChangeBaseTime = input("Do you want to change the base time? (y/n): ")

        if wantToChangeBaseTime == "y":
            days = int(input("How many days ago do you want to start from?"))
            pickedDate = days * 24
            twenty_four_hours_ago = (datetime.now() - timedelta(hours=pickedDate)).isoformat() + "Z"
        else:
            twenty_four_hours_ago = (datetime.now() - timedelta(hours=24)).isoformat() + "Z"
        return twenty_four_hours_ago
        
    def wantToEnterBroadcasterID(self,setTime , game_id, clip_count):
        wantToEnterBroadcasterID = input("Do you want to enter a broadcaster ID? (y/n): ")
        now = datetime.now().isoformat() + "Z"
      
        if wantToEnterBroadcasterID == "y":
            broadcast_id = self.get_broadcastID()
            params = {"started_at": setTime, "ended_at": now, "first": clip_count, "broadcaster_id": broadcast_id}
        else:
            params = {"game_id": game_id, "started_at": setTime,"ended_at":now, "first": clip_count}
        return params

    def get_clips(self, game_id, clip_count):
        setTime = self.change_base_time()
        params = self.wantToEnterBroadcasterID(setTime, game_id, clip_count)
        response = requests.get(self.BASE_URL, headers=self.headers, params=params)
        
        if response.status_code != 200:
            log_error(f"Error fetching clips: {response.text}")
            return []
        
        clips = response.json().get("data", [])
        log_info(f"Fetched {len(clips)} clips.")
        
        return [{"url": clip["url"], "broadcaster_id": clip["broadcaster_id"]} for clip in clips]
    
    
