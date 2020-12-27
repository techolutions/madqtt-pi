from enum import Enum
import logging
import coloredlogs
import itertools


_LoggerEnums = {
    1: ['system', 'SYSTEM'],
    2: ['client', 'CLIENT'],
    3: ['handler', 'HANDLER'],
}
LoggerEnums = Enum(
    value='LoggerEnums',
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _LoggerEnums.items()
    )
)

logging.getLogger("urllib3").propagate = False


def initLogging(config):
    global logger
    coloredlogs.DEFAULT_LOG_FORMAT = '%(asctime)s [%(name)10s] [%(levelname).1s] %(message)s'
    coloredlogs.DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
    coloredlogs.DEFAULT_FIELD_STYLES = {'asctime': {'color': 'cyan'}, 'name': {'bold': True, 'color': 'black'}, 'levelname': {'bold': True, 'color': 'black'}}
    coloredlogs.install(level=config['log']['level'])

def getLogger(type: LoggerEnums):
    logger = logging.getLogger(type.name)
    return logger
