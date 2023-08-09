#!/usr/bin/env python3
"""Basic Auth module"""
from .auth import Auth
from typing import TypeVar
from base64 import b64decode
from models.user import User


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
                return decoded_str.decode('utf-8')
            except Exception:
                return None

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

    def user_object_from_credentials(self, user_email: str, user_pwd: str)\
            -> TypeVar('User'):
        """Returns a user instance based on his email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search(dict(email=user_email))

            if not users or users == []:
                return None

            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieves the User instance for a request"""
        auth_str = self.authorization_header(request)

        if auth_str:
            ext = self.extract_base64_authorization_header(auth_str)

            if ext:
                decode_str = self.decode_base64_authorization_header(ext)

                if decode_str:
                    user_cred = self.extract_user_credentials(decode_str)

                    if user_cred:
                        user = self.user_object_from_credentials(*user_cred)
                        return user
        return
