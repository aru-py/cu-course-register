import requests

from logging import Logger
from logging import Formatter
from logging import LogRecord
from logging import Handler

from logging.handlers import TimedRotatingFileHandler
from logging import StreamHandler

from .io import Colors

logger = Logger(name='primary', level='DEBUG')

# log to files
formatter = Formatter('{asctime:30}' + '{levelname:15}' + '{message}', style='{')
log_file = "logs/register.log"
file_handler = TimedRotatingFileHandler(filename=log_file, when='D', interval=5)  # rotate log file every 5 days
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# send push notification
class IFTTTHandler(Handler):
    """ custom http handler to send ifttt-compatible post requests """

    def __init__(self, url, level='DEBUG'):
        super().__init__(level=level)
        self.url = url

    def emit(self, record: LogRecord) -> None:
        data = {'value1': record.levelname, 'value2': record.getMessage(), 'value3': record.asctime}
        requests.post(url=self.url, data=data)


# add webhooks endpoint as first line to file
key_present = False
with open("config/ifttt.key") as f:
    ifttt_url = f.read()
    if ifttt_url.startswith('http://'):
        key_present = True
http_handler = IFTTTHandler(ifttt_url, level='ERROR')
if key_present:
    logger.addHandler(http_handler)

# log to stderr
formatter = Formatter(Colors.sandstone + Colors.bold + '{message}' + Colors.reset, style='{')
stream_handler = StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel("INFO")
logger.addHandler(stream_handler)
