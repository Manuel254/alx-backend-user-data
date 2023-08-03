#!/usr/bin/env python3
"""Encrypt passwords using bcrypt"""
import bcrypt


def hash_password(password: str) -> str:
    """Returns a salted hashed password"""
    password = bytes(password, encoding='utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt())
