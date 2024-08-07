#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, current_app
from flask_cors import (CORS, cross_origin)
import os
import importlib


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None


auth_type = getenv('AUTH_TYPE', 'None')

if auth_type == 'basic_auth':
    auth_module = importlib.import_module('api.v1.auth.basic_auth')
    AuthClass = getattr(auth_module, 'BasicAuth', None)
    if AuthClass:
        auth = AuthClass()
else:
    auth_module = importlib.import_module('api.v1.auth.auth')
    AuthClass = getattr(auth_module, 'Auth', None)
    if AuthClass:
        auth = AuthClass()


@app.before_request
def before_request():
    """
    This function will be run before each request.
    It will handle authentication and authorization.
    """
    if auth is None:
        return
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                      '/api/v1/forbidden/']
    if not auth.require_auth(request.path, excluded_paths):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def not_authorized(error) -> str:
    """ Unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """forbidden handler"""
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(500)
def internal_server_error(error) -> str:
    """ Internal server error handler """
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
