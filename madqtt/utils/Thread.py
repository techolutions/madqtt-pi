import threading
import time

from .Logging import getLogger, LoggerEnums
logger = getLogger(LoggerEnums.SYSTEM)


class StoppableThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

class RepeatableThread(StoppableThread):

    def __init__(self, waittime, *args, **kwargs):
        super(RepeatableThread, self).__init__(*args, **kwargs)
        self.daemon = True
        self._stop_event = threading.Event()
        self._waittime = waittime

    def run(self):
        while not self.stopped():
            logger.info('%s is working', self.name)
            starttime = time.time()
            self.repeat()
            runtime = time.time() - starttime
            logger.info('%s runtime was %f seconds', self.name, runtime)
            if not self.stopped():
                sleeptime = max(0,self._waittime - runtime)
                logger.info('%s sleeping for %f seconds', self.name, sleeptime)
                self._stop_event.wait(sleeptime)

    def repeat(self):
        pass
