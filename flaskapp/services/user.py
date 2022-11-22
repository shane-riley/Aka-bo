from flaskapp.models import User
from flaskapp.shared import *
from flaskapp.stores import UserStore

from .service import Service

class UserService(Service):
    """
    Service class for users.

    Contains business logic and all things not directly
    route or storage-oriented.
    """

    def __init__(self, user_store: UserStore):
        """
        Create a UserService

        Args:
            user_store (UserStore): Storage implementation to use
        """
        self.user_store = user_store

    def create_user(self, user: User) -> User:
        """
        Create user.

        Args:
            user (User): User to create

        Returns:
            user (User): User created

        Raises:
            DuplicateException: If username exists
            InvalidInputException: If other input issue
            Exception: Other errors
        """

        # Make sure user's inputs exist
        # username, epw, email
        if not (user.username and user.email and user.encrypted_password):
            raise InvalidInputException

        # Check against db
        if self.user_store.get_by_username(user.username):
            raise DuplicateException

        # Add user
        return self.user_store.post_user(user)

    def update_user(self, user: User) -> User:
        """
        Update user.

        Args:
            user (User): User to modify (username exists)

        Returns:
            user (User): User modified

        Raises:
            Exception: If user missing required field (email, username, pw),
            or if user exists
        """

        # Make sure user's inputs exist
        # username, epw, email
        if not (user.username):
            raise InvalidInputException

        # Check against db
        existing_user = self.user_store.get_by_username(user.username)[0]
        if not existing_user:
            raise InvalidInputException

        # Update modifiable fields
        existing_user.bio = user.bio
        return self.user_store.update_user(existing_user)

    def delete_user(self, username: str) -> User:
        """
        Delete user.

        Args:
            username (str): username to remove

        Returns:
            User: Removed user
        """

        # Check username doesn't exist
        if not self.user_store.get_by_username(username):
            raise InvalidInputException

        # Delete
        return self.user_store.delete_by_username(username)