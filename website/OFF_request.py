import requests
import json


class OFFRequest:
    """Retreive data from OpenFactFact and parse them for database insertion"""
    def __init__(self):
        self.data = {}

    def request_constructor(self, search_term):
        url = 'https://fr.openfoodfacts.org/cgi/search.pl?search_terms={}' \
              '&search_simple=1&action=process&nutrition_grades=e' \
              '&sort_by=unique_scans_n&page=1&json=1'.format(search_term)
        r = requests.get(url)
        response = r.json()
        with open('website/OFF_data.json', 'w', encoding='utf-8') as f:
            json.dump(response, f, indent=4)
