import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import vk_api
from vk_api.audio import VkAudio
from getpass import getpass


class MusicFromVKtoYT:
    def __init__(self):
        self.youtube_client = self.get_youtube_client()
        self.vk_client = self.get_vk_client()
        self.all_song_info = {}

    def get_youtube_client(self):
        """ Log Into Youtube, Copied from Youtube Data API """
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        scopes = scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
        credentials = flow.run_console()

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client


    def get_vk_client(self):
        f = True
        while f == True:
            user_login = input("Введите логин или номер телефона ")
            user_password = getpass()
            vk_session = vk_api.VkApi(login = user_login,password = user_password)

            try:
                vk_session.auth()
                f = False
            except vk_api.AuthError as error_msg:
                print("Неверный логин или пароль")
            return vk_session

    def get_vk_songs(self):
        vkaudio = VkAudio(self.vk_client)
        i = 0
        for track in vkaudio.get_iter():
            song_name = track.get('title')
            artist = track.get('artist')
            self.all_song_info[i] = {
                "song_name": song_name,
                "artist": artist
            }
            i += 1


    def create_playlist(self):
        request = self.youtube_client.playlists().insert(
        part="snippet,status",
        body={
          "snippet": {
            "title": "VkMusic",
            "description": "Music from your VK",
            },
          "status": {
            "privacyStatus": "private"
          }
        }
        )
        response = request.execute()
        return response["id"]

    def get_video(self,song_name,artist):
        request = self.youtube_client.search().list(
        part="snippet",
        maxResults=1,
        q= artist +" "+ song_name
        )
        response = request.execute()
        item = response["items"]
        return item[0]["id"]["videoId"]

        

    def add_song_to_playlist(self):
        playlist_id = self.create_playlist()
        self.get_vk_songs()
        for item in self.all_song_info:
            artist = self.all_song_info[item]["artist"]
            song_name = self.all_song_info[item]["song_name"]
            videoID = self.get_video(song_name,artist)
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





if __name__ == '__main__':
    cp = MusicFromVKtoYT()
    print(cp.add_song_to_playlist())

