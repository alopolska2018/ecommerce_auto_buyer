import json, requests
from api_allegro.AllegroRestApi import AllegroRestApi

class GetAllFieldsOfTheParticularOffer:


        def create_headers(self, allegro_api):
            headers = {}
            headers['charset'] = 'utf-8'
            headers['Accept-Language'] = 'pl-PL'
            headers['Content-Type'] = 'application/json'
            headers['Api-Key'] = allegro_api.api_key
            headers['Accept'] = 'application/vnd.allegro.public.v1+json'
            headers['Authorization'] = "Bearer {}".format(allegro_api.access_token)
            return headers

        def get_price_field(self, offer_details):
            price_field = offer_details['sellingMode']['price']['amount']
            return price_field

        def get_offer_price(self, offer_id, account_name):
            allegro_api = AllegroRestApi(account_name)
            api_path = '/sale/offers/{}'.format(offer_id)
            headers = self.create_headers(allegro_api)
            with requests.Session() as session:
                session.headers.update(headers)
                offer_details = session.get(allegro_api.DEFAULT_API_URL + api_path).json()
            price = self.get_price_field(offer_details)
            return price
