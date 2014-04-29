import requests
import json
import logging

from fundingharvest.base import BaseHarvester


class JSONHarvester(BaseHarvester):
    def json_from_http(self, url, params={}):
        r = requests.get(url, params=params)
        return self.load_json(r.text)

    def load_json(self, json_data):
        result = None
        try:
            result = json.loads(json_data)
        except ValueError as e:
            logging.error('Error while loading JSON from {url_with_params}: {msg}'
                            .format(url_with_params=r.request.url, msg=e.message)
            )
        return result
