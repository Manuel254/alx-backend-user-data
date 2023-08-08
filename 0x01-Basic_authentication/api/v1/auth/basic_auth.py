#!/usr/bin/env python3
"""Basic Auth module"""
from .auth import Auth


class BasicAuth(Auth):
    """Creates basic authentication for api"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Return Base64 part of authorization header"""
        if authorization_header is None or not\
                isinstance(authorization_header, str):
            return None
        else:
            my_str = authorization_header.split()

            if len(my_str) < 2:
                return None
            elif my_str[0] != 'Basic':
                return None
            else:
                return my_str[1]
