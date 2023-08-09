#!/usr/bin/env python3
""" Session authentication module"""
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """Handles everything concerning session authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session id fo a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        else:
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
