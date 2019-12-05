import requests, json, os
global session
import keyring

class AllegroRestApi():

    def __init__(self, account_name):
        self.account_name = account_name
        self.DEFAULT_OAUTH_URL = 'https://allegro.pl/auth/oauth'
        self.DEFAULT_API_URL = 'https://api.allegro.pl'
        self.client_id = keyring.get_password('client_id', self.account_name)
        self.api_key = self.client_id
        self.client_secret = keyring.get_password('client_secret', self.account_name)
        self.access_token = keyring.get_password('access_token', self.account_name)
        self.refresh_token = keyring.get_password('refresh_token', self.account_name)
        self.refresh_token_response = ''

        self.do_refresh_token()
        self.get_new_access_token()
        self.get_new_refresh_token()


    def do_refresh_token(self):
        token_url = self.DEFAULT_OAUTH_URL + '/token'

        access_token_data = {'grant_type': 'refresh_token',
                             'api-key': self.api_key,
                             'refresh_token': self.refresh_token}

        response = requests.post(url=token_url,
                                 auth=requests.auth.HTTPBasicAuth(self.client_id, self.client_secret),
                                 data=access_token_data)

        self.refresh_token_response = json.loads(response.content.decode('utf-8'))

    def get_new_access_token(self):
        access_token = self.refresh_token_response['access_token']
        keyring.set_password('access_token', self.account_name, '{}'.format(access_token))
        self.access_token = access_token

    def get_new_refresh_token(self):
        refresh_token = self.refresh_token_response['refresh_token']
        keyring.set_password('refresh_token', self.account_name, '{}'.format(refresh_token))
        self.refresh_token = refresh_token
