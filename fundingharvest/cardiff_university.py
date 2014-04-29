from copy import deepcopy

from fundingharvest.json_harvester import JSONHarvester

API_BASE_URL = 'http://courses.cardiff.ac.uk/FundingJson.aspx'
ORIGIN = 'Cardiff University'


class CardiffHarvester(JSONHarvester):
    feed_url = None
    
    def __init__(self, api_url=API_BASE_URL):
        self.api_url = api_url
        
    def harvest(self):
        records = []

        # the API *needs* an argument, so get Postgraduate Research opportunities first
        data = self.json_from_http(self.api_url, params={"pr": 1})
        records += self.__process_records(data)

        # now get Postgraduate Taught ones
        data = self.json_from_http(self.api_url, params={"pt": 1})
        records += self.__process_records(data)

        return records

    def __process_records(self, data):
        if not data:
            return None
        if not data.get('results'):
            return None

        records = []
        for opportunity in data['results']:
            record = opportunity  # copy all the data by default
            record['origin_id'] = opportunity['id']
            del record['id']  # we generate our own id-s
            record['title'] = opportunity['title']
            record['url'] = opportunity['url']
            record['license'] = self.DEFAULT_COPYRIGHT_LICENSE
            record['origin'] = ORIGIN
            record['origin_method'] = 'harvested'
            record['tags'] = opportunity['levels_of_study'] + opportunity['regions']
            records.append(deepcopy(record))

        return records