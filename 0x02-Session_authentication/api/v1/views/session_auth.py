#!/usr/bin/env python3
"""Handles all routes for session authentication"""
from flask import request, abort, jsonify
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Handles login for user"""
    email = request.form.get('email')
    password = request.form.get('password')

    if email == '' or email is None:
        return jsonify({"error": "email missing"}), 400
    if password == '' or password is None:
        return jsonify({"error": "password missing"}), 400

    users = User.search(dict(email=email))

    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    else:
        for user in users:
            if user.is_valid_password(password):
                from api.v1.app import auth
                session_id = auth.create_session(user.id)
                session_name = getenv('SESSION_NAME')

                res = jsonify(user.to_json())
                res.set_cookie(session_name, session_id)
                return res
        return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """Handles logout for user"""
    from api.v1.app import auth
    destroy_session = auth.destroy_session(request)

    if not destroy_session:
        abort(404)
    else:
        return jsonify({}), 200
