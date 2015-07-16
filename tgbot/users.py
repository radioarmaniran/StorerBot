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

import configparser
import os.path

USER_PATH = configparser.RawConfigParser()
USER_PATH.read('pyapi.cfg')
USER_PATH = USER_PATH.get('General','user_dir')


#def create_conf(user_id):
    #user_file = open(os.path.join(USER_PATH, str(user_id)))
    #user_conf.write(user_file)
    #user_file.close()


def get_conf(user_id):
    user_path = os.path.join(USER_PATH, str(user_id))
    if not os.path.isfile(user_path):
        open(user_path, 'a').close()
    user_conf = configparser.RawConfigParser()
    user_conf.read(user_path)
    return user_conf


def save_conf(user_id, user_conf = None):
    user_file = open(os.path.join(USER_PATH, str(user_id)), 'w')
    if user_conf == None:
        user_conf = configparser.RawConfigParser()
    user_conf.write(user_file)
    user_file.close()


def update_conf(user_id, section, option, value):
    user_conf = get_conf(user_id)
    try:
        user_conf.set(section, option, value)
    except:
        user_conf.add_section(section)
        user_conf.set(section, option, value)
    save_conf(user_id, user_conf)


def get_conf_value(user_id, section, option, value = None):
    try:
        return get_conf(user_id).get(section, option)
    except:
        if value == None:
            return None
        else:
            update_conf(user_id, section, option, value)
            return value
