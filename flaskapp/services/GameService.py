class GameService:
    
    def __init__(self, game_store: GameStore, user_store: UserStore):
        """
        Create a GameService

        Args:
            game_store (GameStore): Game store instance
            user_store (UserStore): User store instance
        """
        self.game_store = game_store
        self.user_store = user_store

    # Create Game
    def create_game(self, game_type: str, player_one: str, player_two: str) -> Game:
        """
        Make a new game

        Args:
            game_type (str): Type to play
            player_one (str): Player one username
            player_two (str): Player two username
        
        Returns:
            game (Game): Game created

        Raises:
            InvalidInputException: If input issue
        """

        # Ensure game_type is valid
        if game_type not in SUPPORTED_GAMES:
            raise InvalidInputException

        # Ensure usernames are valid
        if not self.user_store.get_by_username(player_one):
            raise InvalidInputException
        if not self.user_store.get_by_username(player_two):
            raise InvalidInputException

        # Make a new game
        game = Game(
            game_type=game_type,
            player_one=player_one,
            player_two=player_two
        )

        # Store the game
        return self.game_store.post_game(game)

    # Make move
    def make_move(self, uuid: str, username: str, move: str) -> Game:
        """
        Make a move

        Args:
            uuid (str): Game uuid
            username (str): User making move
            move (str): Move to make (column)

        Returns:
            Game: New Game object
        """

        # Grab game using uuid
        game = self.game_store.get_by_uuid(uuid)

        # Ensure username in game
        if username not in [game.player_one, game.player_two]:
            raise InvalidInputException

        # Ensure user is the one to move
        if ((username == game.player_one and 
            GameState(game.state) != GameState.MOVE_ONE)
            or (username == game.player_two and 
            GameState(game.state) != GameState.MOVE_TWO)):
            raise InvalidInputException

        # Ensure move is legal
        if not Connect4.is_legal(game.board, move):
            raise InvalidInputException

        # Apply move
        new_board = Connect4.apply_move(game.board, move)

        # Check for a win
        new_state = Connect4.check_end(new_board).value

        # Touch
        if GameState(game.state) == GameState.MOVE_ONE:
            game.touch_1()
        else:
            game.touch_2()

        # Update values
        game.board = new_board
        game.state = new_state

        # Update datastore
        return self.game_store.update_game(game)

    # Forfeit game
    def forfeit_game(self, uuid: str, username: str) -> Game:
        """
        Forfeit game

        Args:
            uuid (str): Game uuid
            username (str): username attempting forfeit

        Returns:
            Game: Game forfeited

        Raises:
            InvalidInputException: If username cannot ff at this time,
            or if user not in game
        """

        # Grab game using uuid
        game = self.game_store.get_by_uuid(uuid)

        # Ensure username in game
        if username not in [game.player_one, game.player_two]:
            raise InvalidInputException

        # Can only ff if it is the player's move
        if username == game.player_one and GameState(game.state) != GameState.MOVE_ONE:
            raise InvalidInputException
        if username == game.player_two and GameState(game.state) != GameState.MOVE_TWO:
            raise InvalidInputException

        # ff is valid
        if username == game.player_one:
            game.state = GameState.FF_ONE.value
            game.touch_1()
        if username == game.player_two:
            game.state = GameState.FF_TWO.value
            game.touch_2()
        
        return self.game_store.update_game(game)

    # Poll for update 