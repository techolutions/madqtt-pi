try:
    import RPi.GPIO as GPIO
except:
    pass

from madqtt.utils import *


logger = getLogger(LoggerEnums.HANDLER)

class GpioHandler():

    RELAY_NO = 'NO'
    RELAY_NC = 'NC'

    def __init__(self, channel, relay):
        self._channel = channel
        self._relay = relay
        self.initGpio()

    def __del__(self):
        GPIO.cleanup()

    def initGpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._channel, GPIO.OUT)

    def on(self):
        logger.debug('turning on gpio channel %d(%s)', self._channel, self._relay)
        if self._relay == self.RELAY_NC:
            GPIO.output(self._channel, GPIO.HIGH)
        else:
            GPIO.output(self._channel, GPIO.LOW)

    def off(self):
        logger.debug('turning off gpio channel %d(%s)', self._channel, self._relay)
        if self._relay == self.RELAY_NC:
            GPIO.output(self._channel, GPIO.LOW)
        else:
            GPIO.output(self._channel, GPIO.HIGH)
