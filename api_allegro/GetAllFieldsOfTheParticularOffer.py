import json, requests
from api_allegro.AllegroRestApi import AllegroRestApi

class GetAllFieldsOfTheParticularOffer():

        def __init__(self, account_name):
            self.account_name = account_name
            self.allegro_api = AllegroRestApi(self.account_name)

        def create_headers(self):
            headers = {}
            headers['charset'] = 'utf-8'
            headers['Accept-Language'] = 'pl-PL'
            headers['Content-Type'] = 'application/json'
            headers['Api-Key'] = self.allegro_api.api_key
            headers['Accept'] = 'application/vnd.allegro.public.v1+json'
            headers['Authorization'] = "Bearer {}".format(self.allegro_api.access_token)
            return headers

        def get_price_field(self, offer_details):
            price_field = offer_details['sellingMode']['price']['amount']
            return price_field

        def get_user_info(self):
            api_path = '/me'
            headers = self.create_headers()
            with requests.Session() as session:
                session.headers.update(headers)
                user_details = session.get(self.allegro_api.DEFAULT_API_URL + api_path).json()
            return user_details
        def get_offer_price(self, offer_id):
            api_path = '/sale/offers/{}'.format(offer_id)
            headers = self.create_headers()
            with requests.Session() as session:
                session.headers.update(headers)
                offer_details = session.get(self.allegro_api.DEFAULT_API_URL + api_path).json()
            price = self.get_price_field(offer_details)
            return price
