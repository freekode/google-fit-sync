import requests
import json
import date_utils
from datetime import datetime

class TodaysPlan:
    username = None;
    password = None;
    token = '';
    user = None;

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authorize(self):
        r = requests.post('https://whats.todaysplan.com.au/rest/auth/login',
            data = json.dumps({
                'username': self.username,
                'password': self.password,
                'token': 'true'
            }),
            headers = self.get_headers())

        content = json.loads(r.content)

        self.token = content['token'];
        self.user = content['user'];

    def test(self):
        r = requests.get('https://whats.todaysplan.com.au/rest/auth/whoami', headers = self.get_headers())
        return r.status_code is 200

    def set_weight(self, value, timestamp):
        user_id = self.user['id']
        dt = datetime.fromtimestamp(timestamp)
        year = dt.year;
        day_number = date_utils.get_day_number(dt);

        url = 'https://whats.todaysplan.com.au/rest/users/day/set/{}/{}/{}'.format(user_id, year, day_number)
        r = requests.post(url,
            data = json.dumps({
                'att': {
                    "ts": timestamp * 1000,
                    'weight': value
                },
                'flag': 0
            }),
            headers = self.get_headers())

        return r.content

    def sync_weights(self, values):
        for value in values:
            print(self.set_weight(value['value'], value['time']))

    def get_headers(self):
        return {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }
