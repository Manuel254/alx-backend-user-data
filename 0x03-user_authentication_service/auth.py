#!/usr/bin/env python3
"""Hash password"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt"""
    password = password.encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    return hashed
