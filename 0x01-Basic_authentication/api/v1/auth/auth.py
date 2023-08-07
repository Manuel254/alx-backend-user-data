#!/usr/bin/env python3
"""Authentication module"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Creates authentication for api"""
    def require_auth(self, path:str, excluded_paths: List[str]) -> bool:
        """Checks to see if path requires authentication"""
        return False

    def authorization_header(self, request=None) -> str:
        """Authorization header of a particular request"""
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user of api"""
        return request
