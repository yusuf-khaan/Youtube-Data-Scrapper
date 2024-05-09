import os
import json
import googleapiclient.discovery
from googleapiclient.errors import HttpError

class YouTubeDataInterface:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=self.api_key)

    def fetch_video_info(self, channel_info_file, max_results=50, output_folder=None):
        video_data = []
        
        try:
            with open(channel_info_file) as f:
                channel_info = json.load(f)

            for entry in channel_info:
                channel_id = entry.get("channel_id")

                if channel_id:
                    try:
                        search_request = self.youtube.search().list(
                            part="snippet",
                            type="video",
                            maxResults=max_results,
                            channelId=channel_id
                        )

                        all_videos = []
                        next_page_token = None

                        while True:
                            search_response = search_request.execute()
                            video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]

                            if video_ids:
                                video_request = self.youtube.videos().list(
                                    part="snippet",
                                    id=",".join(video_ids)
                                )
                                video_response = video_request.execute()
                                all_videos.extend(video_response.get("items", []))

                            if "nextPageToken" in search_response:
                                next_page_token = search_response["nextPageToken"]
                                search_request = self.youtube.search().list(
                                    part="snippet",
                                    type="video",
                                    maxResults=max_results,
                                    pageToken=next_page_token,
                                    channelId=channel_id
                                )
                            else:
                                break

                        for item in all_videos:
                            title = item["snippet"]["title"]
                            description = item["snippet"]["description"]
                            video_data.append({"Title": title, "Description": description})
                    except HttpError as e:
                        if e.resp.status == 403:
                            print("Quota exceeded for API key:", self.api_key)
                            break
                        else:
                            raise
                else:
                    print("Channel ID not found in JSON entry.")

            if output_folder:
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                with open(os.path.join(output_folder, 'video_info.json'), 'w') as json_file:
                    json.dump(video_data, json_file)
                print("Video information saved to video_info.json")
            else:
                return video_data

        except FileNotFoundError:
            print("Channel info JSON file not found.")
        except Exception as e:
            print("An error occurred:", e)

# Example usage:
if __name__ == "__main__":
    api_key = "AIzaSyDkLxDZJXqTC9POiJvb9pth8iY5pU_j08g"
    channel_info_file = "G:/Jarvis/JarvisAI/Channel IDs/channel_info.json"
    max_results = 50
    output_folder = "G:/Jarvis/JarvisAI/Database"

    youtube_interface = YouTubeDataInterface(api_key)
    youtube_interface.fetch_video_info(channel_info_file, max_results, output_folder)
