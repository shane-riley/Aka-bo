from typing import List

from flaskapp.models import User
from .store import Store

class UserStore(Store):
    """
    Storer class for users using Google Cloud DataStore

    NOTE: Inherits Store for general methods
    """

    def __init__(self, client):
        super().__init__(client)

    def post_user(self, user: User) -> User:
        """
        Add a user to datastore

        Args:
            user (User): User to add

        Returns:
            User: User added
        """
        return super().post_object(User, user)

    def update_user(self, user: User) -> User:
        """
        Update user that exists

        Args:
            user (User): User to update

        Returns:
            User: User updated
        """
        return super().update_object(User, user, 'uid', user.uid)

    def get_by_uid(self, uid: str) -> User:
        """
        Get a list of users matching the uid

        Args:
            uid (str): uid to match

        Returns:
            User:
        """
        u = super().get_objects_by_field(User, 'uid', uid)
        return u[0] if len(u) else None

    def uid_exists(self, uid: str) -> bool:
        """
        Check whether uid exists in table

        Args:
            uid (str): user id

        Returns:
            bool: whether exists in table
        """
        return len(super().get_objects_by_field(User, 'uid', uid)) > 0

    def username_exists(self, username: str) -> bool:
        """
        Check whether username exists in table

        Args:
            username (str): public username

        Returns:
            bool: whether exists in table
        """
        return len(super().get_objects_by_field(User, 'username', username)) > 0

    def delete_by_uid(self, uid: str) -> None:
        """
        Delete a list of users matching the uid

        Args:
            uid (str): uid to match

        Returns:
            User: Deleted user
        """
        u = super().delete_by_field(User, 'uid', uid)
        return u[0] if len(u) else None