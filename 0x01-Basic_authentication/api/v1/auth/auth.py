#!/usr/bin/env python3
"""auth.py
"""

from flask import request
from typing import List, TypeVar

User = TypeVar('User')


class Auth:
    """auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if the given path requires authentication.
        :param path: The path to check
        :param excluded_paths:list of paths not require authentication
        :return: False (default implementation)
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        cleaned_path = path.rstrip('/')
        for excluded_path in excluded_paths:
            cleaned_excluded_path = excluded_path.rstrip('/')
            if cleaned_path == cleaned_excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request.
        :param request: The request object
        :return: None (default implementation)
        """
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        return auth_header

    def current_user(self, request=None) -> User:
        """
        Retrieves the current user from the request.
        :param request: The request object
        :return: None (default implementation)
        """
        return None
