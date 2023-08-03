#!/usr/bin/env python3
"""Obfuscates field in data"""
from typing import List
import re
import logging


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns a string with field obfuscated by redaction"""
    for field in fields:
        pattern = r'(?<={}=)(.+?)(?={})'.format(field, separator)
        message = re.sub(pattern, redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters incoming message and logs it with a format"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """Returns a logging object"""
    logger = getLogger('user_data')
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger
