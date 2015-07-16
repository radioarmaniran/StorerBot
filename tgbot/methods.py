#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Raúl Jornet Calomarde'
__contact__ = 'rjornetc@openmailbox.org'
__copyright__ = 'Copyright © 2015, Raúl Jornet Calomarde'
__license__ = '''License GPLv3+: GNU GPL version 3 or any later
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or any later version. This program
is distributed  in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU General Public License for more details.
<http://www.gnu.org/licenses/>'''
__date__ = '2015-06-25'
__version__ = '0.0'

import urllib.parse
import urllib.request
import configparser
import json


#CONFIG = configparser.RawConfigParser()
LAST_UPDATE_ID = 0


TOKEN = configparser.RawConfigParser()
TOKEN.read('pyapi.cfg')
TOKEN = TOKEN.get('General','token')


def _send_method(method, arguments = ""):
    arguments = urllib.parse.urlencode(arguments)
    binary_data = arguments.encode('ascii')
    path = 'https://api.telegram.org/bot' + TOKEN + '/' + method
    print('================\n' + path + '&' + str(binary_data) + '\n================')
    req = urllib.request.Request(path, binary_data)
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    response = urllib.request.urlopen(req).read().decode('ascii')
    #print(response)
    out = json.loads(response)
    return out


def get_me():
    return _send_method('getme')


def send_message(chat_id,
                 text,
                 disable_web_page_preview = None,
                 reply_to_message_id = None,
                 reply_markup = None):
    arguments = {'chat_id': chat_id,
                 'text': text}
    if disable_web_page_preview:
        arguments['disable_web_page_preview'] = disable_web_page_preview
    if reply_to_message_id:
        arguments['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        arguments['reply_markup'] = json.dumps(reply_markup)

    return _send_method('sendmessage', arguments)


def get_updates(offset = None,
                limit = None,
                timeout = None):
    arguments = {}
    if offset:
        arguments['offset'] = offset
    if limit:
        arguments['limit'] = limit
    if timeout:
        arguments['timeout'] = timeout

    if len(arguments) == 0:
        return _send_method('getupdates')
    else:
        return _send_method('getupdates', arguments)


def get_last_updates():
    global LAST_UPDATE_ID
    out = get_updates(LAST_UPDATE_ID+1)
    if len(out['result']) > 0:
        LAST_UPDATE_ID = out['result'][-1]['update_id']
    return out


def forward_message(chat_id,
                    from_chat_id,
                    message_id):
    arguments = {'chat_id': chat_id,
                 'from_chat_id': from_chat_id,
                 'message_id': message_id}

    return _send_method('sendmessage', arguments)


def send_photo(chat_id,
               photo,
               caption = None,
               reply_to_message_id = None,
               reply_markup = None):
    arguments = {'chat_id': chat_id,
                 'photo': photo}

    if caption:
        arguments['caption'] = caption

    if reply_to_message_id:
        arguments['reply_to_message_id'] = reply_to_message_id

    if reply_markup:
        arguments['reply_markup'] = json.dumps(reply_markup)

    return _send_method('sendphoto', arguments)


def send_audio(chat_id,
               audio,
               reply_to_message_id = None,
               reply_markup = None):
    arguments = {'chat_id': chat_id,
                 'audio': audio}

    if reply_to_message_id:
        arguments['reply_to_message_id'] = reply_to_message_id

    if reply_markup:
        arguments['reply_markup'] = json.dumps(reply_markup)

    return _send_method('sendaudio', arguments)


def send_document(chat_id,
                  document,
                  reply_to_message_id = None,
                  reply_markup = None):
    arguments = {'chat_id': chat_id,
                 'document': document}

    if reply_to_message_id:
        arguments['reply_to_message_id'] = reply_to_message_id

    if reply_markup:
        arguments['reply_markup'] = json.dumps(reply_markup)

    return _send_method('senddocument', arguments)


def send_sticker(chat_id,
                 sticker,
                 reply_to_message_id = None,
                 reply_markup = None):
    arguments = {'chat_id': chat_id,
                 'sticker': sticker}

    if reply_to_message_id:
        arguments['reply_to_message_id'] = reply_to_message_id

    if reply_markup:
        arguments['reply_markup'] = json.dumps(reply_markup)

    return _send_method('sendmessage', arguments)


def send_video(chat_id,
               video,
               reply_to_message_id = None,
               reply_markup = None):
    arguments = {'chat_id': chat_id,
                 'video': video}

    if reply_to_message_id:
        arguments['reply_to_message_id'] = reply_to_message_id

    if reply_markup:
        arguments['reply_markup'] = json.dumps(reply_markup)

    return _send_method('sendmessage', arguments)


def send_chat_action(chat_id,
                     action):
    arguments = {'chat_id': chat_id,
                 'action': action}

    return _send_method('sendchataction', arguments)


def send_location(chat_id,
                  latitude,
                  longitude):
    arguments = {'chat_id': chat_id,
                 'latitude': latitude,
                 'longitude': longitude}

    return _send_method('sendlocation', arguments)


def get_user_profile_photos(user_id,
                            offset = None,
                            limit = None):
    arguments = {'user_id': user_id }

    if offset:
        arguments['offset'] = offset

    if limit:
        arguments['limit'] = limit

    return _send_method('getuserprofilephotos', arguments)


def forward_message(chat_id,
                    from_chat_id,
                    message_id):
    arguments = {'chat_id': int(chat_id),
                 'from_chat_id': int(from_chat_id),
                 'message_id': int(message_id)}

    return _send_method('forwardmessage', arguments)


last_update_id = get_updates(0,1)['result']
if len(last_update_id) > 0:
    LAST_UPDATE_ID = last_update_id[-1]['update_id']
#print(LAST_UPDATE_ID)
