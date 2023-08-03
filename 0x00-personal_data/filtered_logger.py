#!/usr/bin/env python3
"""Obfuscates field in data"""
from typing import List
import re
import logging
import mysql.connector
import os


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns a string with field obfuscated by redaction"""
    for field in fields:
        pattern = r'(?<={}=)(.+?)(?={})'.format(field, separator)
        message = re.sub(pattern, redaction, message)
    return message


def get_logger() -> logging.Logger:
    """Returns a logging object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a mysql connector"""
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')

    connection = mysql.connector.connection.MySQLConnection(host=host,
                                                            database=db_name,
                                                            user=username,
                                                            password=password)
    return connection


def main():
    """Displays data from database"""
    message = 'name={}; email={}; phone={}; ssn={}; password={}; ip={}; \
last_login={}; user_agent={};'
    logger = get_logger()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")

    data = cur.fetchall()

    for row in data:
        name, email, phone, ssn, password,\
            ip, last_login, user_agent = row
        logger.info(message.format(name, email, phone, ssn, password, ip,
                                   last_login, user_agent))


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


if __name__ == '__main__':
    main()
