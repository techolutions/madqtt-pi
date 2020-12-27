from datetime import datetime
from .Exceptions import *

def ut2ts(unixtime):
    return datetime.utcfromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')

def shutdown(signum, frame):
    raise ServiceExit
