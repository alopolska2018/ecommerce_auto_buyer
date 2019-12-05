import json, requests
import uuid

from api_allegro import AllegroRestApi

class ModifyBuyNowPrice():
    def generate_uuid(self):
        command_id = uuid.uuid4()
        return str(command_id)

    def create_data_dict(self, command_id, price):
        data = {}
        data['id'] = command_id
        input = {}
        buy_now_price = {}
        buy_now_price['amount'] = price
        buy_now_price['currency'] = 'PLN'
        data['input'] = input
        input['buyNowPrice'] = buy_now_price
        return data

    def create_headers(self, allegro_api):
        headers = {}
        headers['charset'] = 'utf-8'
        headers['Accept-Language'] = 'pl-PL'
        headers['Content-Type'] = 'application/vnd.allegro.public.v1+json'
        headers['Api-Key'] = allegro_api.api_key
        headers['Accept'] = 'application/vnd.allegro.public.v1+json'
        headers['Authorization'] = "Bearer {}".format(allegro_api.access_token)
        return headers

    def modify_price(self, offer_id, price, account_name):
        allegro_api = AllegroRestApi.AllegroRestApi(account_name)
        headers = self.create_headers(allegro_api)
        command_id = self.generate_uuid()
        api_path = '/offers/{}/change-price-commands/{}'.format(offer_id, command_id)
        data = self.create_data_dict(command_id, price)

        with requests.Session() as session:
            session.headers.update(headers)
            response = session.put(allegro_api.DEFAULT_API_URL + api_path, json=data).json()
            return response
