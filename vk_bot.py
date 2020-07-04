#!/usr/bin/python3
# -*- coding: utf-8 -*-

import vk_api
from vk_api.utils import get_random_id
from vk_api.longpoll import *

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,'random_id':get_random_id()}) #send message to user with user_id
    
#ur group token
token = "20af1c32866b2cf0c59d670b18dc0b23cd6dbbdac15cfd0d6cbcd306a2d392a368afbce410bd79834af4a"

# Auth as community
vk = vk_api.VkApi(token=token)

# work with message
longpoll = VkLongPoll(vk)

# main cicle

def main():            

    for event in longpoll.listen():
        # if new message
        if event.type == VkEventType.MESSAGE_NEW:#if new message
            # if its for me
            if event.to_me: #if message for me
                bots_dialogs = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter":'unanswered'})#Taking all chats with unanswered status(structure of returned obj in docs: https://vk.com/dev/messages.getConversations )
                for dialog in bots_dialogs['items']:
                    from_id = dialog['last_message']['from_id'] #id of use
                    try: 
                        geo = dialog['last_message']['geo'] #geo object in last message (structure of geo in docs: https://vk.com/dev/objects/geo )
                        longitude = geo['coordinates']['longitude'] #longitude 
                        latitude = geo['coordinates']['latitude']#latitude
                    except KeyError:#if there are no geo in the message then except KeyError
                        print("there are no geo in the message")
                    atchs = dialog['last_message']['attachments']#taking attachments in last message (structure of atch in docs: https://vk.com/dev/objects/attachments_m )
                    for atch in atchs:
                        if atch["type"] == "photo" : # if there are photo in the attachments then we take it
                            url = atch["photo"]["sizes"][6]["url"] #6 - format of image(all formats:0 - 9)
                            write_msg(from_id, url) #echo url of photo
                text = event.text
                if text == "end": #stop-word (for tests)
                    return
                if text != '':
                    write_msg(from_id, text) #echo text
main()