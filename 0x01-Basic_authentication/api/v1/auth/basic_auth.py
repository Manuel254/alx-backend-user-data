#!/usr/bin/env python3
"""Basic Auth module"""
from .auth import Auth
from base64 import b64decode


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str)\
            -> str:
        """Returns the decoded value of a Base64 string
        base64_authorization_header
        """
        if base64_authorization_header is None or not\
                isinstance(base64_authorization_header, str):
            return None
        else:
            try:
                decoded_str = b64decode(base64_authorization_header)
            except Exception:
                return None
            return decoded_str.decode('utf-8')

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str)\
            -> (str, str):
        """Returns the user email and password from
        the Base64 decoded value
        """
        if decoded_base64_authorization_header is None\
                or not isinstance(decoded_base64_authorization_header, str)\
                or ':' not in decoded_base64_authorization_header:
            return (None, None)
        else:
            my_str = decoded_base64_authorization_header.split(':')
            return (my_str[0], my_str[1])
