import requests
from selectorlib import Extractor


class Temperature:

    def __init__(self, country, city):
        self.country = country.replace(' ', '-').lower()
        self.city = city.replace(' ', '-').lower()

    def _build_url(self):
        url = requests.get(f'https://www.timeanddate.com/weather/{self.country}/{self.city}')
        return url

    def _scrape(self):
        url = self._build_url().text
        extractor = Extractor.from_yaml_file('static/temperature.yaml')
        raw_result = extractor.extract(url)
        return raw_result

    def get(self):
        scraped_content = self._scrape()
        result = float(scraped_content['temp'].replace('\xa0°C', '').strip())
        return result
