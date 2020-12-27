import json
import time
import copy

from madqtt.utils import *

from .GpioHandler import GpioHandler
from .RestHandler import RestHandler
from .CmdHandler import CmdHandler


logger = getLogger(LoggerEnums.HANDLER)

class DeviceHandler():

    STATE_ON  = 'on'
    STATE_OFF = 'off'

    def __init__(self):
        self._devices = copy.deepcopy(config['devices'])

        for device in self._devices:
            if self._devices[device]['mode'] == 'gpio':
                handler = GpioHandler(self._devices[device]['channel'], self._devices[device]['relay'])
            elif self._devices[device]['mode'] == 'rest':
                handler = RestHandler(self._devices[device]['switchon'], self._devices[device]['switchoff'])
            elif self._devices[device]['mode'] == 'cmd':
                handler = CmdHandler(self._devices[device]['switchon'], self._devices[device]['switchoff'])
            else:
                raise Exception('mode {0} for device {1} is unknown'.format(self._devices[device]['mode'], device))
            self._devices[device]['handler'] = handler

            self.on(device)

    def on(self, device):
        logger.info('turning %s on', device)
        try:
            self._devices[device]['handler'].on()
            self.setState(device, self.STATE_ON)
        except:
            logger.error('error occured while turning on device %s', device)
        finally:
            return self.getState(device)

    def off(self, device):
        logger.info('turning %s off', device)
        try:
            self._devices[device]['handler'].off()
            self.setState(device, self.STATE_OFF)
        except:
            logger.error('error occured while turning off device %s', device)
        finally:
            return self.getState(device)

    def toggle(self, device):
        logger.info('toggle %s', device)
        if self.getState(device) == self.STATE_ON:
            return self.off(device)
        else:
            return self.on(device)

    def exists(self, device):
        return device in self._devices

    def setState(self, device, state):
        self._devices[device]['state'] = state

    def getState(self, device):
        return self._devices[device]['state']

    def getSetup(self, device):
        setup = {}
        setup['device'] = device
        if self.exists(device):
            setup = {**setup, **config['devices']}
        return json.dumps(setup)

    def getDeviceList(self):
        devices = []
        for device in self._devices:
            devices.append(device)
        return devices
