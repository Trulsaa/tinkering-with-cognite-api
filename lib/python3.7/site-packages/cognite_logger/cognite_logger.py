import logging
from datetime import datetime

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        # Set timestamp
        now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        log_record["timestamp"] = log_record.get("timestamp", now)
        # Set severity
        severity = log_record.get("level", record.levelname)
        log_record["severity"] = severity.upper()
        # Set sourceLocation
        source_location = {
            "file": record.filename,
            "function": record.funcName,
            "line": record.lineno,
            "loggerName": record.name,
            "threadName": record.threadName,
            "thread": record.thread,
        }
        log_record["sourceLocation"] = source_location


def get_standard_text_formater():
    return logging.Formatter(
        "%(asctime)s.%(msecs)03d [%(levelname)-8s] %(threadName)s. %(message)s (%(filename)s:%(lineno)s)",
        "%Y-%m-%d %H:%M:%S",
    )


def configure_logger(
    logger_name: str, log_level: str, log_json: bool, replace_handler: bool = True, filters=None, filename: str = None
):
    """
    Configure logger
    :param logger_name: Name of the logger. None for root logger.
    :param log_json: bool Flag for logging json or not
    :param log_level: Log level. E.g. "DEBUG"
    :param replace_handler: Set to true if this new handler should replace any already on the logger
    :param filters: List of filters to add to log handler.
    :param filename: Set to filename if logging should be done to file
    :return: Logger
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    if replace_handler:
        logger.handlers = []
        logger.propagate = False
    if filename is None:
        log_handler = logging.StreamHandler()
    else:
        log_handler = logging.FileHandler(filename)
    if log_json:
        formatter = CustomJsonFormatter()
    else:
        formatter = get_standard_text_formater()
    log_handler.setFormatter(formatter)
    if filters and isinstance(filters, list):
        for current in filters:
            log_handler.addFilter(current)

    logger.addHandler(log_handler)

    return logger
