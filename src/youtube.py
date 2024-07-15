import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

class YouTubeClient:
    def __init__(self):
        self.youtube_client = self.get_youtube_client()
        self.songs = []

    def get_youtube_client(self):
        
        scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client


    def create_playlist(self):
        name = input("Введите имя плэйлиста: ")
        description = input("Введите описание плэйлиста: ")
        request = self.youtube_client.playlists().insert(
        part="snippet,status",
        body={
          "snippet": {
            "title": name,
            "description": description,
            },
          "status": {
            "privacyStatus": "private"
          }
        }
        )
        response = request.execute()
        return response["id"]
 
    
    def get_list_of_songs(self,url):
        playlist_id = url.replace("https://www.youtube.com/playlist?list=",'')

        request = self.youtube_client.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id
        )

        response = request.execute()
        try:
            nextPageToken = response["nextPageToken"]
        except KeyError:
            nextPageToken = None

        while nextPageToken:
            request = self.youtube_client.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                pageToken = response["nextPageToken"]
                )
            
            response = request.execute()
            for i in response["items"]:
                self.songs.append(i["snippet"]["title"])
            try:
                nextPageToken = response["nextPageToken"]
            except KeyError:
                nextPageToken = None
        
        return self.songs      


    def search_song(self,song_name):
        request = self.youtube_client.search().list(
        part="snippet",
        maxResults=1,
        q= song_name
        )
        response = request.execute()
        item = response["items"]
        return item[0]["id"]["videoId"]

    def add_songs_to_playlist(self,songs):
        playlist_id = self.create_playlist()
        for item in songs:
            videoID = self.get_video(item)
            request = self.youtube_client.playlistItems().insert(
            part="snippet",
            body={
            "snippet": {
            "playlistId": str(playlist_id),
            "position": 0,
            "resourceId": {
              "kind": "youtube#video",
              "videoId": str(videoID)
                    }
                }
            }
        )        
            response = request.execute()
            a = []
            a.append(response)
        return a