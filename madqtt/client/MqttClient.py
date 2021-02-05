import paho.mqtt.client as mqtt
import re
import time
import threading

from madqtt.utils import *
from madqtt.handler.DeviceHandler import DeviceHandler

logger = getLogger(LoggerEnums.CLIENT)

class MqttClient(StoppableThread):

    def __init__(self, *args, **kwargs):
        super(MqttClient, self).__init__(*args, **kwargs)
        self.daemon = True
        self.name = 'MqttClient'
        self._client = mqtt.Client()
        self._client.on_connect = self.on_connect
        self._client.on_disconnect = self.on_disconnect
        self._client.on_message = self.on_message

        if config['mqtt']['broker']['tls']['enabled'] == True:
            self._client.tls_set()

        if config['mqtt']['broker']['auth']['enabled'] == True:
            self._client.username_pw_set(config['mqtt']['broker']['user'], config['mqtt']['broker']['pass'])

        self._deviceHandler = DeviceHandler()

    def stop(self):
        self._client.disconnect()

    def run(self):
        logger.info('trying to connect to mqtt broker %s:%d', config['mqtt']['broker']['host'], config['mqtt']['broker']['port'])
        self._client.connect(config['mqtt']['broker']['host'], config['mqtt']['broker']['port'], 30)
        self._client.loop_forever(retry_first_connection=True)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info('connection successful')
            logger.info('subscribing to topic "%s/#"', config['mqtt']['topic'])
            client.subscribe('{0}/#'.format(config['mqtt']['topic']))
            client.message_callback_add('{0}/command'.format(config['mqtt']['topic']), self.on_command)
            client.message_callback_add('{0}/+/command'.format(config['mqtt']['topic']), self.on_device_command)
            self.update()
        else:
            raise ConnectionError('connection to mqtt broker failed with rc {0}'.format(rc))

    def on_disconnect(self, client, userdata, rc):
        if rc == 0:
            logger.info('disconnection successful')
        else:
            logger.error('disconnection unexpected')

    def on_message(self, client, userdata, message):
        pass

    def on_command(self, client, userdata, message):
        command = message.payload.decode('UTF-8')
        logger.debug('%s > %s', message.topic, command)

        if command == 'announce':
            self.announce()
        elif command == 'update':
            self.update()
        elif command == 'on':
            self.on()
        elif command == 'off':
            self.off()
        elif command == 'toggle':
            self.toggle()
        elif command == 'restart':
            self.restart()
        else:
            logger.warning('command "%s" is unknown', command)

    def on_device_command(self, client, userdata, message):
        command = message.payload.decode('UTF-8')
        logger.debug('%s > %s', message.topic, command)

        device = re.match(r'^{}\/(.*)\/command$'.format(config['mqtt']['topic']), message.topic).group(1)
        if self._deviceHandler.exists(device):
            if command == 'on':
                self.on(device)
            elif command == 'off':
                self.off(device)
            elif command == 'toggle':
                self.toggle(device)
            elif command == 'restart':
                self.restart(device)
            else:
                logger.warning('command "%s" is unknown', command)


    def _buildDevices(self, device = None):
        devices = []
        if device == None:
            devices = self._deviceHandler.getDeviceList()
        elif self._deviceHandler.exists(device):
            devices.append(device)
        return devices

    def update(self, device = None):
        for device in self._buildDevices(device):
            threading.Thread(target=self.updateThread, args=(device,)).start()

    def announce(self, device = None):
        for device in self._buildDevices(device):
            threading.Thread(target=self.announceThread, args=(device,)).start()

    def on(self, device = None):
        for device in self._buildDevices(device):
            threading.Thread(target=self.onThread, args=(device,)).start()

    def off(self, device = None):
        for device in self._buildDevices(device):
            threading.Thread(target=self.offThread, args=(device,)).start()

    def toggle(self, device = None):
        for device in self._buildDevices(device):
            threading.Thread(target=self.toggleThread, args=(device,)).start()

    def restart(self, device = None):
        for device in self._buildDevices(device):
            threading.Thread(target=self.restartThread, args=(device,)).start()


    def updateThread(self, device):
        state = self._deviceHandler.getState(device)
        self._client.publish('{0}/{1}'.format(config['mqtt']['topic'], device), state)

    def announceThread(self, device):
        setup = self._deviceHandler.getSetup(device)
        self._client.publish('{0}/announce'.format(config['mqtt']['topic']), setup)
        self._client.publish('{0}/{1}/announce'.format(config['mqtt']['topic'], device), setup)

    def onThread(self, device):
        state = self._deviceHandler.on(device)
        self._client.publish('{0}/{1}'.format(config['mqtt']['topic'], device), state)

    def offThread(self, device):
        state = self._deviceHandler.off(device)
        self._client.publish('{0}/{1}'.format(config['mqtt']['topic'], device), state)

    def toggleThread(self, device):
        state = self._deviceHandler.toggle(device)
        self._client.publish('{0}/{1}'.format(config['mqtt']['topic'], device), state)

    def restartThread(self, device):
        self.offThread(device)
        time.sleep(5)
        self.onThread(device)
