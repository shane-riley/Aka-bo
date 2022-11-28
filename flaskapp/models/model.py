from flaskapp.shared import *

class Model:
    """
    BaseClass for Model objects

    May only contain properties legal as value types for GCloud Datastore:
    - strings
    - ints
    - floats
    - bools
    - datetimes
    """

    def serialize(self):
        """
        Make json representation

        NOTE: Because of dynamic reasons, this method can see subclass attributes

        Returns:
            dictionary json response
        """

        # Use default
        return self.__dict__
