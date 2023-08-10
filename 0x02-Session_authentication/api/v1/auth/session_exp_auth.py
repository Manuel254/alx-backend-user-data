#!/usr/bin/env python3
""" Session expiration module"""
from .session_auth import SessionAuth
import datetime
from os import getenv


class SessionExpAuth(SessionAuth):
    """Handles everything concerning session expiration"""

    def __init__(self):
        """Instantiation"""
        try:
            session_duration = int(getenv('SESSION_DURATION'))

            if not session_duration:
                self.session_duration = 0
            else:
                self.session_duration = session_duration
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Creates session"""
        session_id = super().create_session(user_id)

        if not session_id:
            return None

        session_dictionary = {
                'user_id': user_id,
                'created_at': datetime.datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        print(self.user_id_by_session_id)
        print(session_id)
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get user id for session id"""
        session_dict = self.user_id_by_session_id

        if session_id is None or session_id not in session_dict:
            return None

        user_id = session_dict.get(session_id).get('user_id')

        if self.session_duration <= 0:
            return user_id

        created_at = session_dict.get(session_id).get('created_at')
        time = created_at + datetime.timedelta(seconds=self.session_duration)

        if not created_at:
            return None
        if time < datetime.datetime.now():
            return None

        return user_id
