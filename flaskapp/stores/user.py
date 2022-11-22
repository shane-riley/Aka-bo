from typing import List

from flaskapp.models import User
from .store import Store

class UserStore(Store):
    """
    Storer class for users using Google Cloud DataStore

    NOTE: Inherits Store for general methods
    """

    def __init__(self):
        pass

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
        return super().update_object(User, user, 'username', user.username)

    def get_by_username(self, username: str) -> List[User]:
        """
        Get a list of users matching the username

        Args:
            username (str): Username to match

        Returns:
            List[User]: Length=1 list of users
        """
        return super().get_objects_by_field(User, 'username', username)

    def delete_by_username(self, username: str) -> None:
        """
        Delete a list of users matching the username

        Args:
            username (str): Username to match

        Returns:
            List[User]: Length=1 list of users
        """
        return super().delete_by_field(User, 'username', username)[0]