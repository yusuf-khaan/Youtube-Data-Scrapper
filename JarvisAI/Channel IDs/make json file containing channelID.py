import json
import os
import re
from googleapiclient.discovery import build

class YouTubeChannelInfoExtractor:
    def __init__(self, api_key):
        self.api_key = api_key

    def extract_channel_info(self, video_url):
        video_id_match = re.search(r"(?<=v=)[\w-]+", video_url)
        if video_id_match:
            video_id = video_id_match.group(0)
        else:
            print("Invalid YouTube video URL.")
            return

        youtube = build("youtube", "v3", developerKey=self.api_key)

        try:
            video_response = youtube.videos().list(
                part="snippet",
                id=video_id
            ).execute()

            channel_id = video_response["items"][0]["snippet"]["channelId"]
            channel_name = video_response["items"][0]["snippet"]["channelTitle"]
            return channel_id, channel_name

        except Exception as e:
            print("An error occurred:", str(e))
            return None, None

    def extract_channel_info_from_json(self, json_file):
        with open(json_file) as f:
            data = json.load(f)
            video_links = data["videos"]

        channel_info_list = []
        for video_link in video_links:
            channel_id, channel_name = self.extract_channel_info(video_link)
            if channel_id and channel_name:
                channel_info_list.append({
                    "video_link": video_link,
                    "channel_id": channel_id,
                    "channel_name": channel_name
                })
        return channel_info_list

    def save_channel_info_to_json(self, channel_info_list, output_path):
        output_file = os.path.join(output_path, 'channel_info.json')
        with open(output_file, 'w') as f:
            json.dump(channel_info_list, f, indent=4)
        print("Channel information has been saved to:", output_file)

if __name__ == "__main__":
    # Your API key
    api_key = "AIzaSyDkLxDZJXqTC9POiJvb9pth8iY5pU_j08g"
    
    # Specify the location of the JSON file containing video links
    json_file_path = "G:/Jarvis/JarvisAI/Channel IDs/videos.json"

    # Specify the output path for the channel information JSON file
    output_path = "G:/Jarvis/JarvisAI/Channel IDs"

    extractor = YouTubeChannelInfoExtractor(api_key)
    channel_info_list = extractor.extract_channel_info_from_json(json_file_path)
    extractor.save_channel_info_to_json(channel_info_list, output_path)
