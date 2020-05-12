from random import randint
from vk_api.longpoll import VkLongPoll, VkEventType
from UsersRequest import UsersRequest
from requests import post
from Parametrs import *
import vk
import vk_api


class VKBot:
    def __init__(self):
        self.api = vk.API(vk.Session(access_token=VK_API_TOKEN))
        self.longpoll = VkLongPoll(vk_api.VkApi(token=VK_API_TOKEN))
        self.users_request = UsersRequest()
        self.requesting_picture = False

    def run(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    bot_message, requesting_picture = self.users_request.get_answer(event.text)

                    if requesting_picture:
                        self.write_message_with_picture(event.user_id, bot_message)
                    else:
                        self.write_message(event.user_id, bot_message)

    def write_message(self, user_id, message):
        self.api.messages.send(
            user_id=user_id, random_id=randint(0, 2048),
            message=message,
            v=VK_API_VERSION
        )

    def write_message_with_picture(self, user_id, message):
        upload_server = self.api.photos.getMessagesUploadServer(peer_id=user_id, v=VK_API_VERSION)['upload_url']
        response_json = post(upload_server, files={'photo': open(GRAPH_NAME, 'rb')}).json()
        photo = self.api.photos.saveMessagesPhoto(
            server=response_json['server'],
            photo=response_json['photo'],
            hash=response_json['hash'],
            v=VK_API_VERSION
        )[0]
        self.api.messages.send(
            user_id=user_id, random_id=randint(0, 2048),
            message=message,
            attachment="photo{}_{}".format(photo['owner_id'], photo['id']),
            v=VK_API_VERSION
        )
