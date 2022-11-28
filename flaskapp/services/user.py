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

    def get_user(self, uid: str) -> User:
        """
        Load user from uid

        Args:
            uid (str): unique identifier

        Returns:
            User: coressponding user object
        """

        # Confirm uid
        if not uid:
            raise InvalidInputException

        u = self.user_store.get_by_uid(uid)

        # Throw if no match
        if not u:
            raise NoMatchException

        return self.user_store.get_by_uid(uid)

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
        # username, uid, email
        if not (user.username and user.email and user.uid):
            raise InvalidInputException

        # Check against db
        if self.user_store.get_by_uid(user.uid):
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

        # Make sure user's uid exist
        if not (user.uid):
            raise InvalidInputException

        # Check against db
        existing_user = self.user_store.get_by_uid(user.uid)
        if not existing_user:
            raise InvalidInputException

        # Update modifiable fields
        existing_user.bio = user.bio
        return self.user_store.update_user(existing_user)

    def delete_user(self, uid: str) -> User:
        """
        Delete user.

        Args:
            uid (str): unique user identifier

        Returns:
            User: Removed user
        """

        # Check uid doesn't exist
        if not self.user_store.uid_exists(uid):
            raise InvalidInputException

        # Delete
        return self.user_store.delete_by_uid(uid)