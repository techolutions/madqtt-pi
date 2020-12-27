import subprocess

from madqtt.utils import *


logger = getLogger(LoggerEnums.HANDLER)

class CmdHandler():

    def __init__(self, switchon, switchoff):
        self._switchon = switchon
        self._switchoff = switchoff

    def on(self):
        logger.debug('sending command "%s"', self._switchon)
        subprocess.run(self._switchon, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def off(self):
        logger.debug('sending command "%s"', self._switchoff)
        subprocess.run(self._switchoff, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
