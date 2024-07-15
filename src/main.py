#import os

from youtube import YouTubeClient
from vk import VKClient

if __name__ == '__main__':
    vk = VKClient()
    youtube = YouTubeClient()
    youtube.songs = vk.get_vk_songs()
    youtube.add_songs_to_playlist()

