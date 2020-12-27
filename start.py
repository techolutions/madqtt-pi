import signal
import time

from madqtt.utils import *
from madqtt.client.MqttClient import MqttClient


logger = getLogger(LoggerEnums.SYSTEM)

def main():
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    logger.info('*** starting madqtt ***')

    threads = []
    threads.append(MqttClient())

    [t.start() for t in threads]
    while True in [t.is_alive() for t in threads]:
        try:
            [t.join() for t in threads]
        except ServiceExit:
            print()
            logger.debug('stopping all threads')
            [t.stop() for t in threads]

    logger.info('*** stopped madqtt ***')

if __name__ == "__main__":
    main()
