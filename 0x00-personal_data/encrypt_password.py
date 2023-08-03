#!/usr/bin/env python3
"""Encrypt passwords using bcrypt"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted hashed password"""
    password = bytes(password, encoding='utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a password is valid"""
    password = bytes(password, encoding='utf-8')
    if bcrypt.checkpw(password, hashed_password):
        return True
    return False
