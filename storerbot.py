import sys
from tgbot import methods
from tgbot import users
from ast import literal_eval
import threading
from datetime import datetime
import re


DEFAULT_FOLDER = {
    'mime_type':'folder',
    'icon':None,
    'content':{}}

DEFAULT_FOLDER_STRUCTURE = {
    'mime_type':'folder',
    'icon':None,
    'content':{
        'Audios':{
            'mime_type':'folder',
            'icon':None,
            'content':{}},
        'Images':{
            'mime_type':'folder',
            'icon':None,
            'content':{}},
        'Gifs':{
            'mime_type':'folder',
            'icon':None,
            'content':{}},
        'Stickers':{
            'mime_type':'folder',
            'icon':None,
            'content':{}},
        'Videos':{
            'mime_type':'folder',
            'icon':None,
            'content':{}},
        'Documents':{
            'mime_type':'folder',
            'icon':None,
            'content':{}},
        'Messages':{
            'mime_type':'folder',
            'icon':None,
            'content':{}}
    }
}

EMOJIS = (8419,  169,   174,   8194,  8195,  8197,  8252,  8265,
          8482,  8505,  8596,  8597,  8598,  8599,  8600,  8601,
          8617,  8618,  8986,  8987,  9194,  9195,  9196,  9200,
          9203,  9410,  9642,  9643,  9654,  9664,  9723,  9724,
          9725,  9726,  9728,  9729,  9742,  9745,  9748,  9749,
          9757,  9786,  9800,  9801,  9802,  9803,  9804,  9805,
          9806,  9807,  9808,  9809,  9810,  9811,  9824,  9827,
          9829,  9830,  9832,  9851,  9855,  9875,  9888,  9889,
          9898,  9899,  9917,  9918,  9924,  9925,  9934,  9940,
          9962,  9970,  9971,  9973,  9978,  9981,  9986,  9989,
          9992,  9993,  9994,  9995,  9996,  9999,  10002, 10004,
          10006, 10024, 10035, 10036, 10052, 10055, 10060,
          10062, 10067, 10068, 10069, 10071, 10084, 10133,
          10134, 10135, 10145, 10160, 10548, 10549, 11013,
          11014, 11015, 11035, 11036, 11088, 11093, 12336,
          12349, 12951, 12953)

DEFAULT_FULL_MIMETYPE_ICONS = {'application/epub+zip':'📖',
                               'application/octet-stream':'⬛',
                               'application/pdf':'📕',
                               'audio/midi':'🎼',
                               'audio/x-midi':'🎼',
                               'application/certificate':'📝',
                               'application/dicom':'🔬',
                               'application/javascript':'🔨',
                               'application/pgp-encrypted':'🔒',
                               'application/pgp-keys':'🔐',
                               'application/pgp-signature':'🔏',
                               'application/pkcs7-mime':'🔒',
                               'application/pkcs7-signature':'🔏',
                               'application/vnd.ms-publisher':'🔑',
                               'application/vnd.oasis.opendocument.spreadsheet':'📊',
                               'application/x-executable':'💡',
                               'application/x-java-archive':'☕️',
                               'application/x-ms-dos-executable':'💩',
                               'application/x-pem-key':'🔐',
                               'application/x-php':'🔨',
                               'application/x-sharedlib':'⬛',
                               'application/x-shellscript':'🐧',
                               'application/x-shockwave-flash':'🎬',
                               'application/x-trash':'♻️',
                               'application/x-compressed-tar':'📦',
                               'application/x-wine-extension-ini':'🍷',
                               'application/zip':'📦',
                               'folder':'📁',
                               'image/gif':'🎡',
                               'image/jpeg':'🌇',
                               'image/png':'🌌',
                               'image/svg+xml':'➰',
                               'image/webp':'🌀',
                               'telegram/audio':'🔈',
                               'telegram/contact':'👤',
                               'text/css':'🎨',
                               'text/html':'🌐',
                               'text/x-c++src':'👾',
                               'text/x-csrc':'👾',
                               'text/x-makefile':'🔨',
                               'text/x-markdown':'📓',
                               'text/x-python':'🐍'}

DEFAULT_MIMETYPE_ICONS = {'message':'💬',
                          'audio':'🎵',
                          'text':'📄',
                          'image':'🌇',
                          'video':'🎬',
                          'location':'📍',
                          'application':'🔴'}

DEFAULT_ICON = '❔'


def position_to_path(position):
    path = '/'
    for folder in position:
        path += folder + '/'
    return path


def is_empty(storage):
    if len(storage.keys()) == 0:
        return True
    return False

def display_folder(chat_id,storage,position,selection = None):

    storage = get_element(storage,position)['content']
    elements = list(storage.keys())
    elements = sorted(elements, key=lambda s: s.lower())
    folder_elements = []
    file_elements = []

    for element in elements:
        if storage[element]['mime_type'] == 'folder':
            folder_elements.append(element)
        else:
            file_elements.append(element)
    elements = folder_elements + file_elements
    print(elements)
    message = position_to_path(position)

    if selection != None:
        keyboard = [['✖️End selection','▪ Select all','▫ Unselect all']]

        if len(selection) > 0:
            if len(selection) == 1:
                keyboard.append(['✏ Rename','🔵 Change icon','ℹ Properties','❌ Remove','📑 Copy','✂ Cut'])
            else:
                keyboard.append(['❌ Remove','📑 Copy','✂ Cut'])
    else:
        keyboard = [['➕ Folder']]
        if not is_empty(storage):
            keyboard[0].append('☑ Select')
        clipboard = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'clipboard', '{}'))
        if not clipboard == {}:
            keyboard[0].append('📋 Paste')

    if position == [] or selection != None:
        responses = {}
    else:
        keyboard.append(['⬆ ..'])
        responses = {'⬆ ..':'..'}

    for element in elements:
        icon = storage[element]['icon']
        if icon == None:
            try:
                icon = DEFAULT_FULL_MIMETYPE_ICONS[storage[element]['mime_type']]
            except KeyError:
                not_full_icons = set(literal_eval(users.get_conf_value('recolection', 'General', 'not-full-icons', '{}')))
                not_full_icons.add(storage[element]['mime_type'])
                users.update_conf('recolection', 'General', 'not-full-icons', not_full_icons)
                try:
                    icon = DEFAULT_MIMETYPE_ICONS[storage[element]['mime_type'].split('/')[0]]
                except KeyError:
                    not_icons = set(literal_eval(users.get_conf_value('recolection', 'General', 'not-icons', '{}')))
                    not_icons.add(storage[element]['mime_type'])
                    users.update_conf('recolection', 'General', 'not-icons', not_icons)
                    icon = DEFAULT_ICON

        if selection == None:
            line = icon + ' ' + element

        elif element in selection:
            line = '🔳 ' + icon + ' ' + element
        else:
            line = '◻ ' + icon + ' ' + element

        message += '\n' + line
        responses[line] = element
        keyboard.append([line])


    users.update_conf(chat_id, 'General', 'responses', responses)
    methods.send_message(chat_id,
                         message,
                         reply_markup = {'keyboard':keyboard,
                                         'resize_keyboard':True})

def has_emojis(string):
    for character in string:
        if (is_a_emoji(character)):
            return True
    return False

def is_a_emoji(string):
    if ord(string) >= 126980 or ord(string) in EMOJIS:
        return True
    else:
        return False


def get_element(storage,element_path):
    try:
        for folder in element_path:
            storage = storage['content'][folder]
        return storage
    except KeyError:
        return None


def set_element(storage,element_path,element,k=None):
    keys = ''
    for folder in element_path:
        keys += '[\'content\'][\'' + folder + '\']'
    for key in element.keys():
        if type(element[key]) == str:
            value = '\'' + element[key] + '\''
        else:
            value = str(element[key])
        if k:
            print('storage' + str(keys) + '[\'' + str(k) + '\'][\'' + str(key) + '\']=' + str(value))
            exec('storage' + keys + '[\'' + k + '\'][\'' + key + '\']=' + value)
        else:
            exec('storage' + keys + '[\'' + key + '\']=' + value)

    return storage


def del_element(storage,element_path):
    keys = ''
    for folder in element_path:
        keys += '[\'content\'][\'' + folder + '\']'
    exec('del storage' + keys )


def copy_elements(chat_id, storage, position, selected):
    clipboard = {}
    for element in selected:
        clipboard[element] = get_element(storage,position + [element])
    users.update_conf(chat_id, 'General',
                    'clipboard', clipboard)


def protect_string(string):
    return string.replace('\\','\\\\').replace('\'','\\\'').replace('\n','')


def open_element(chat_id,element_path):
    storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))
    if element_path[-1] == '..':
        element_path = element_path[0:-2]
    element = get_element(storage,element_path)
    if element:
        if element['mime_type'] == 'folder':
            users.update_conf(chat_id, 'General', 'position', element_path)
            display_folder(chat_id,storage,element_path)
        elif element['mime_type'] == 'audio/telegram':
            methods.send_audio(chat_id,
                               element['file_id'])
            display_folder(chat_id,storage,element_path[0:-1])
        elif element['mime_type'] == 'telegram/contact':
            profile_photo = methods.get_user_profile_photos(element['user_id'],limit = 1)
            print(profile_photo['result']['photos'][0])
            methods.send_photo(chat_id,
                               profile_photo['result']['photos'][0][0]['file_id'],
                               element['first_name'] + ' ' + element['last_name'] + '\n' +\
                                    '+' + element['phone_number'],)
            methods.send_message(chat_id,
                                 element['first_name'] + ' ' + element['last_name'] + '\n' +\
                                    '+' + element['phone_number'] + '\n' +\
                                    str(element['user_id']))
        else:
            methods.send_document(chat_id,
                                  element['file_id'])
            display_folder(chat_id,storage,element_path[0:-1])
    else:
        methods.send_message(chat_id, '⚠ ' + position_to_path(element_path) + ' does not exists')
        display_folder(chat_id,
                       storage,
                       literal_eval(users.get_conf_value(chat_id, 'General',
                                                         'position', '[]')))


def perform(chat_id, text):
    position = literal_eval(users.get_conf_value(chat_id, 'General',
                                                 'position', '[]'))

    task = users.get_conf_value(chat_id, 'General',
                                'task', '')

    responses = literal_eval(users.get_conf_value(chat_id, 'General',
                                        'responses', '{}'))
    try:
        text = responses[text]
    except KeyError:
        pass

    if text == '/start':
        storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))
        display_folder(chat_id,storage,position)
    elif task == '☑':
        selected = literal_eval(users.get_conf_value(chat_id, 'General',
                                                 'selected', '[]'))

        storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))

        responses =literal_eval(users.get_conf_value(chat_id, 'General',
                                         'responses', '{}'))
        try:
            text = responses[text]
        except KeyError:
            pass

        text = text.replace(chr(65039),'')

        if is_a_emoji(text[0]):
            code = text[0]
        else:
            code = None

        if code == '✖':
            users.update_conf(chat_id, 'General',
                          'task', '')
            users.update_conf(chat_id, 'General',
                          'selected', '[]')
            display_folder(chat_id,storage,position)
        elif code == '▪':
            selected = list(get_element(storage,position)['content'].keys())
            users.update_conf(chat_id, 'General',
                          'selected', str(selected))
            display_folder(chat_id,storage,position,selected)
        elif code == '▫':
            selected = []
            users.update_conf(chat_id, 'General',
                          'selected', '[]')
            display_folder(chat_id,storage,position,selected)
        elif code == '❌':
            for element in selected:
                element = protect_string(element)
                del_element(storage,position + [element])

            users.update_conf(chat_id, 'General',
                              'storage', str(storage))
            users.update_conf(chat_id, 'General',
                          'task', '')
            users.update_conf(chat_id, 'General',
                          'selected', '[]')
            display_folder(chat_id,storage,position)

        elif code == '📑':
            copy_elements(chat_id, storage, position, selected)
            users.update_conf(chat_id, 'General',
                          'task', '')
            users.update_conf(chat_id, 'General',
                          'selected', '[]')
            display_folder(chat_id,storage,position)

        elif code == '✂':
            copy_elements(chat_id, storage, position, selected)
            for element in selected:
                element = protect_string(element)
                del_element(storage,position + [element])
            users.update_conf(chat_id, 'General',
                              'storage', str(storage))
            users.update_conf(chat_id, 'General',
                          'task', '')
            users.update_conf(chat_id, 'General',
                          'selected', '[]')
            display_folder(chat_id,storage,position)

        elif code == '✏' and len(selected) == 1:
            users.update_conf(chat_id, 'General',
                            'task', '✏')
            methods.send_message(chat_id, 'Insert a new name:',reply_markup = {'keyboard': [['✖ Cancel']],
                                            'resize_keyboard':True})
            users.update_conf(chat_id, 'General', 'position', position + selected)
        elif code == '🔵' and len(selected) == 1:
            users.update_conf(chat_id, 'General',
                            'task', '🔵')
            methods.send_message(chat_id, 'Send an emoji:',reply_markup = {'keyboard': [['🔵 Default','✖ Cancel']],
                                            'resize_keyboard':True})
            users.update_conf(chat_id, 'General', 'position', position + selected)
        elif code == 'ℹ' and len(selected) == 1:
            users.update_conf(chat_id,
                              'General',
                              'position',
                              position + selected)



            methods.send_message(chat_id, '⛔ Not implemented')
        elif text in get_element(storage,position)['content']:
            if text in selected:
                selected.remove(text)
            else:
                selected.append(text)
            users.update_conf(chat_id, 'General',
                          'selected', selected)
            display_folder(chat_id,storage,position,selected)
        else:
            methods.send_message(chat_id, '⚠ ' + text + ' does not exists')
    elif task == '✏':
        if text[0] == '✖':
            storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))
            users.update_conf(chat_id, 'General', 'position', position[0:-1])
            users.update_conf(chat_id, 'General', 'task', '')
            users.update_conf(chat_id, 'General', 'selected', '[]')
            display_folder(chat_id,storage,position[0:-1])
        elif text == '.' or text == '..':
            methods.send_message(chat_id, '⛔ Name can not be "." or ".."\nInsert another folder name:')
        elif has_emojis(text):
            methods.send_message(chat_id, '⛔ Name can not contain emojis\nInsert another folder name:')
        else:
            storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))
            element = get_element(storage,position)
            if text in get_element(storage,position[0:-1])['content'].keys():
                methods.send_message(chat_id, '⛔ There is already a folder named ' + text + '\nInsert another folder name:')
            else:
                print(storage,position[0:-1],{text:element})
                storage = set_element(storage,position[0:-1],{text:element},'content')
                del_element(storage,position)
                users.update_conf(chat_id, 'General', 'storage', str(storage))
                users.update_conf(chat_id, 'General', 'position', position[0:-1])
                users.update_conf(chat_id, 'General', 'task', '')
                users.update_conf(chat_id, 'General', 'selected', '[]')
                display_folder(chat_id,storage,position[0:-1])

    elif task == '🔵':
        if is_a_emoji(text[0]) and len(text) == 1:
            storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))
            storage = set_element(storage,position,{'icon':text})
            users.update_conf(chat_id, 'General', 'storage', str(storage))
            users.update_conf(chat_id, 'General', 'position', position[0:-1])
            users.update_conf(chat_id, 'General', 'task', '')
            users.update_conf(chat_id, 'General', 'selected', '[]')
            display_folder(chat_id,storage,position[0:-1])
        elif text == '✖ Cancel':
            storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))
            users.update_conf(chat_id, 'General', 'position', position[0:-1])
            users.update_conf(chat_id, 'General', 'task', '')
            users.update_conf(chat_id, 'General', 'selected', '[]')
            display_folder(chat_id,storage,position[0:-1])
        elif text == '🔵 Default':
            storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))
            storage = set_element(storage,position,{'icon':None})
            users.update_conf(chat_id, 'General', 'storage', str(storage))
            users.update_conf(chat_id, 'General', 'position', position[0:-1])
            users.update_conf(chat_id, 'General', 'task', '')
            users.update_conf(chat_id, 'General', 'selected', '[]')
            display_folder(chat_id,storage,position[0:-1])
        else:
            methods.send_message(chat_id, '⛔ Icon must be an emoji')

    elif task == '➕':
        if text[0] == '✖':
            storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))
            users.update_conf(chat_id, 'General',
                          'task', '')
            display_folder(chat_id,storage,position)
        elif text == '.' or text == '..':
            methods.send_message(chat_id, '⛔ Name can not be "." or ".."\nInsert another folder name:')
        elif has_emojis(text):
            methods.send_message(chat_id, '⛔ Name can not contain emojis\nInsert another folder name:')
        else:
            storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))
            text=protect_string(text)
            if text in get_element(storage,position)['content'].keys():
                methods.send_message(chat_id, '⛔ There is already a folder named ' + text + '\nInsert another folder name:')
            else:
                new_folder = {text:DEFAULT_FOLDER}
                storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                    'storage', str(DEFAULT_FOLDER_STRUCTURE)))
                storage = set_element(storage,position,new_folder,'content')
                users.update_conf(chat_id, 'General',
                            'task', '')
                users.update_conf(chat_id, 'General',
                            'storage', storage)
                display_folder(chat_id,storage,position)

    elif text[0] == '➕':
        users.update_conf(chat_id, 'General',
                          'task', '➕')
        methods.send_message(chat_id, 'Insert folder name:',reply_markup = {'keyboard': [['✖ Cancel']],
                                         'resize_keyboard':True})
    elif text[0] == '☑':
        storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                'storage', str(DEFAULT_FOLDER_STRUCTURE)))
        selected = literal_eval(users.get_conf_value(chat_id, 'General',
                                                 'selected', '[]'))
        users.update_conf(chat_id, 'General',
                          'task', '☑')
        display_folder(chat_id,storage,position,selected)
    elif text[0] == '📋':
        clipboard = literal_eval(users.get_conf_value(chat_id, 'General',
                                                      'clipboard', '{}'))
        if clipboard == {}:
            methods.send_message(chat_id,'⚠ There is nothing to paste in the clipboard')
        else:
            storage = literal_eval(users.get_conf_value(chat_id, 'General',
                                                        'storage', str(DEFAULT_FOLDER_STRUCTURE)))

            elements = get_element(storage,position)['content'].keys()

            name_error = False

            for clipboard_element in clipboard.keys():
                if clipboard_element in elements:
                    clipboard[correct(clipboard_element)] = clipboard[clipboard_element]
                    del clipboard[clipboard_element]

            if name_error:
                methods.send_message(chat_id, '⛔ There is already a file named ' + name_error + '\nRename the folder before paste')
            else:
                storage = set_element(storage,position,clipboard,'content')
                users.update_conf(chat_id, 'General',
                            'clipboard', '{}')
                users.update_conf(chat_id, 'General',
                            'storage', storage)
        display_folder(chat_id,storage,position)
    else:
        responses =literal_eval(users.get_conf_value(chat_id, 'General',
                                         'responses', '{}'))
                                         
        try:
            text = responses[text]
        except KeyError:
            pass
            
        open_element(chat_id,position + [text])


def document_sended(chat_id, document):
    task = users.get_conf_value(chat_id, 'General',
                                'task', '')
    if task == '':
        storage = literal_eval(users.get_conf_value(chat_id,
                                                    'General',
                                                    'storage',
                                                    str(DEFAULT_FOLDER_STRUCTURE)))
        position = literal_eval(users.get_conf_value(chat_id, 'General',
                                                 'position', '[]'))

        file_name = document['file_name']
        document['icon'] = None

        if file_name in get_element(storage,position)['content'].keys():
            file_name = correct(file_name)


        storage = set_element(storage,position,{file_name:document},'content')
        users.update_conf(chat_id, 'General',
                            'storage', storage)
        display_folder(chat_id,storage,position)


def correct(file_name):
    file_name = file_name.split('.')
    print(file_name)
    if len(file_name) == 1:
        matches = re.findall('\((\d+)\)$',file_name[0])
        print(matches)
        if matches == []:
            file_name = file_name[0] + '(1)'
        else:
            file_name = re.findall('(.*)\(\d+\)$',file_name[0])[0] + '(' + str(int(matches[0])+1) + ')'
    else:
        matches = re.findall('\((\d+)\)$',file_name[0])
        print(matches)
        if matches == []:
            file_name = file_name[0] + '(1).' + file_name[1]
        else:
            file_name = re.findall('(.*)\(\d+\)$',file_name[0])[0] + '(' + str( int(matches[0]) + 1 ) + ').' + file_name[1]
    return file_name


def run():
    running = True
    while running:
        try:
            updates = methods.get_last_updates()
        except KeyboardInterrupt:
            print('\nout')
            quit()
        except:
            pass
        for update in updates['result']:
            try:
                if 'text' in update['message'].keys():
                    threading.Thread(
                        target=perform(
                            int(update['message']['chat']['id']),
                            update['message']['text'])
                        ).start()
                elif 'audio' in update['message'].keys():
                    audio = update['message']['audio']
                    audio['file_name'] =  format(datetime.now(),'audio_%Y-%m-%d_%H-%M-%S.ogg')
                    audio['mime_type'] = 'audio/telegram'
                    threading.Thread(
                        target=document_sended(
                            int(update['message']['chat']['id']),
                            audio)
                        ).start()
                elif 'document' in update['message'].keys():
                    threading.Thread(
                        target=document_sended(
                            int(update['message']['chat']['id']),
                            update['message']['document'])
                        ).start()
                elif 'photo' in update['message'].keys():
                    chat_id = int(update['message']['chat']['id'])
                    methods.send_message(chat_id, '⛔ To save an image attach it as a file (uncompressed), not as a photo')
                    display_folder(chat_id,
                                literal_eval(users.get_conf_value(chat_id,
                                                        'General',
                                                        'storage',
                                                        str(DEFAULT_FOLDER_STRUCTURE))),
                                literal_eval(users.get_conf_value(chat_id, 'General',
                                                    'position', '[]')))
                elif 'sticker' in update['message'].keys():
                    sticker = update['message']['sticker']
                    sticker['file_name'] = format(datetime.now(),'sticker_%Y-%m-%d_%H-%M-%S.webp')
                    sticker['mime_type'] = 'image/webp'
                    threading.Thread(
                        target=document_sended(
                            int(update['message']['chat']['id']),
                            sticker)
                        ).start()
                elif 'contact' in update['message'].keys():
                    contact = update['message']['contact']
                    contact['file_name'] = contact['first_name'] + ' ' + contact['last_name']
                    contact['mime_type'] = 'telegram/contact'
                    threading.Thread(
                        target=document_sended(
                            int(update['message']['chat']['id']),
                            contact)
                        ).start()
                else:
                    chat_id = int(update['message']['chat']['id'])
                    methods.send_message(chat_id, '⛔ Unsuported media')
                    display_folder(chat_id,
                                literal_eval(users.get_conf_value(chat_id,
                                                        'General',
                                                        'storage',
                                                        str(DEFAULT_FOLDER_STRUCTURE))),
                                literal_eval(users.get_conf_value(chat_id, 'General',
                                                    'position', '[]')))

            except:
                methods.send_message(int(update['message']['chat']['id']),
                                     str(sys.exc_info()))



if __name__ == '__main__':
    run()
