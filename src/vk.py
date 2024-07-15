import vk_api
from vk_api.audio import VkAudio
from getpass import getpass


class VKClient:
    def __init__(self):
        self.vk_client = self.get_vk_client()
        self.songs = []
    
    def __auth_handler():
        """ При двухфакторной аутентификации вызывается эта функция.
        """

        # Код двухфакторной аутентификации
        key = input("Enter authentication code: ")
        # Если: True - сохранить, False - не сохранять.
        remember_device = True

        return key, remember_device
    
    def get_vk_client(self):
        f = True
        while f:
            user_login = input("Введите логин или номер телефона ")
            user_password = getpass()
            vk_session = vk_api.VkApi(login = user_login,password = user_password,auth_handler=self.__auth_handler)

            try:
                vk_session.auth()
                f = False
                print("Welcome")
            except vk_api.AuthError as error_msg:
                print(error_msg)
        return vk_session
    
    def get_vk_songs(self):
        vkaudio = VkAudio(self.vk_client)
        i = 0
        for track in vkaudio.get_iter():
            song_name = track.get('title')
            artist = track.get('artist')
            self.songs[i] = artist + song_name
            i += 1
        return self.songs
