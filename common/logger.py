import logging
import time
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record['timestamp'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(record.created))
        log_record['level'] = record.levelname
        if 'message' not in log_record:
            log_record['message'] = record.getMessage()

def setup_logger():
    logger = logging.getLogger("MiniDNSResolver")
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler("output.log")
    fh.setLevel(logging.DEBUG)

    formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(message)s')

    fh.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(fh)

    return logger
