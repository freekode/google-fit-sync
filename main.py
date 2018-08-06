#!/usr/bin/env python3

import json
import date_utils
import sys
import getopt
from google import Google
from todaysplan import TodaysPlan

settings_filename = 'settings.json'
settings = None;
google = None;
todaysplan = None;

def init_google():
    global google

    token = None
    if 'google' in settings:
        token = settings['google']
    google = Google(token);

    settings['google'] = google.token
    save_settings();

def init_todaysplan():
    global todaysplan

    todaysplan = TodaysPlan(settings['todaysplan']['username'], settings['todaysplan']['password'])
    todaysplan.authorize()

def init_settings():
    global settings

    try:
        file = open(settings_filename, 'r')
        file_content = json.load(file);
    except IOError:
        file = open(settings_filename, 'w+')
        file_content = {}

    file.close();

    settings = file_content;

def save_settings():
    with open(settings_filename, 'w') as file:
        json.dump(settings, file)

def main():
    global client_id
    global settings
    global google

    init_settings();
    init_google();
    init_todaysplan();

    user_info = google.get_user_info()
    print('email:', user_info['email'])

    start_sec, end_sec = date_utils.get_start_end_from_args(sys.argv);

    weight_values = google.get_user_weight(start_sec, end_sec);
    print('weight:', weight_values)

    todaysplan.sync_weights(weight_values);

if __name__ == '__main__':
    main()
