from typing import List, Optional

from flaskapp.models import Game
from .store import Store

class GameStore(Store):
    """
    Class for storing Games
    """

    def __init__(self, client):
        super().__init__(client)
    
    def post_game(self, game: Game) -> Game:
        """
        Add a game to datastore

        Args:
            game (Game): Game to add

        Returns:
            Game: Game added
        """
        return super().post_object(Game, game)

    def update_game(self, game: Game) -> Game:
        """
        Update a game that exists

        Args:
            game (Game): Game to update

        Returns:
            Game: Game updated
        """

        # Game uuid is the key
        return super().update_object(Game, game, 'uuid', game.uuid)

    def get_by_uuid(self, uuid: str) -> Optional[Game]:
        """
        Get Game matching uuid or None if no matches

        Args:
            uuid (str): Unique identifier

        Returns:
            Optional[Game]: Game or None
        """
        return super().get_object_by_field(Game, 'uuid', uuid)
    
    def get_by_uid(self, uid: str) -> List[Game]:
        """
        Get user's games

        Args:
            uid (str): unique use identifier

        Returns:
            List[Game]: Games for uid
        """
        return super().get_objects_by_field(Game, 'player_one', uid).extend(
               super().get_objects_by_field(Game, 'player_two', uid))
    
    def delete_by_uuid(self, uuid: str) -> Optional[Game]:
        """
        Delete Game matching uuid or None

        Args:
            uuid (str): Unique identifier

        Returns:
            Optional[Game]: Game or None
        """
        return super().delete_by_field(Game, 'uuid', uuid)[0]