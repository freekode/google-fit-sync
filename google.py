from requests_oauthlib import OAuth2Session
import json
import time
from datetime import datetime
from datetime import timedelta

scope = [
    "https://www.googleapis.com/auth/fitness.body.read",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile"
]

client_id_filename = 'client_id.json'


class Google:
    client_id = None;
    token = None;
    session = None;

    def __init__(self, token=None):
        self.token = token;
        self.client_id = self.get_client_id();
        self.session = self.get_google_session();

    def get_client_id(self):
        file = open(client_id_filename, 'r')
        file_content = json.load(file);
        file.close();

        return file_content

    def get_google_session(self):
        session = None;

        if not self.token:
            session = self.get_oauth_session();
            self.token = get_token()

        session = self.get_oauth_session(self.token);

        body = 'client_secret={}&client_id={}'.format(self.client_id['installed']['client_secret'], self.client_id['installed']['client_id'])

        self.token = session.refresh_token(
            self.client_id['installed']['token_uri'],
            body=body)

        return session

    def get_token(self):
        authorization_url, state = self.session.authorization_url(
            self.client_id['installed']['auth_uri'],
            access_type="offline")
        print(authorization_url)

        authorization_code = raw_input('input code:')

        self.session.fetch_token(
            token_url=self.client_id['installed']['token_uri'],
            client_secret=self.client_id['installed']['client_secret'],
            code=authorization_code)

        return google.token

    def get_oauth_session(self, token=None):
        return OAuth2Session(
            self.client_id['installed']['client_id'],
            scope=scope,
            redirect_uri=self.client_id['installed']['redirect_uris'][0],
            token=token)

    def get(self, url):
        r = self.session.get(url)
        return json.loads(r.content)

    def get_user_weight(self, timestamp_start, timestamp_end):
        start_ns = timestamp_start * 1000 * 1000 * 1000
        end_ns = timestamp_end * 1000 * 1000 * 1000

        url = 'https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.weight:com.google.android.gms:merge_weight/datasets/{}-{}'.format(start_ns, end_ns)

        data = self.get(url)

        values = []
        for point in data['point']:
            value = round(point['value'][0]['fpVal'], 2)
            time = int(point['modifiedTimeMillis']) / 1000
            values.append({
                'time': time,
                'value': value
            })

        return values

    def get_user_info(self):
        return self.get('https://www.googleapis.com/oauth2/v1/userinfo')
