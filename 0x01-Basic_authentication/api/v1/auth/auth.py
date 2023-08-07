#!/usr/bin/env python3
"""Authentication module"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Creates authentication for api"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks to see if path requires authentication"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        for item in excluded_paths:
            if item.startswith(path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Request Validation"""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user of api"""
        return None
