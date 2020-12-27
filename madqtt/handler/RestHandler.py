import requests

from madqtt.utils import *


logger = getLogger(LoggerEnums.HANDLER)

class RestHandler():

    def __init__(self, switchon, switchoff):
        self._switchon = switchon
        self._switchoff = switchoff

    def on(self):
        logger.debug('sending request "%s"', self._switchon)
        r = requests.get(self._switchon)
        if r.status_code != 200:
            raise Exception('http request failed')

    def off(self):
        logger.debug('sending request "%s"', self._switchoff)
        r = requests.get(self._switchoff)
        if r.status_code != 200:
            raise Exception('http request failed')
