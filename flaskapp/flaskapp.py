import flask
from flaskapp.services import GameService, MatchService, UserService
from flaskapp.stores import GameStore, MatchStore, UserStore
from google.cloud import datastore

class Akabo(flask.Flask):
    """
    Class for Backend Flask app
    """

    def __init__(self, name):
        """
        Instantiate the flask app

        Args:
            name (str): name of app
        """

        # Run flask ops
        super().__init__(name)

        # Run setup
        self.setup_services()
        self.setup_routes()

    def setup_services(self):
        """
        Add services to app
        """

        us = UserStore(datastore.Client())
        gs = GameStore(datastore.Client())
        ms = MatchStore(datastore.Client())

        self.user_service = UserService(us)
        self.match_service = MatchService(gs, ms, us)
        self.game_service = GameService(gs, us)
    
    def setup_routes(self):
        """
        Setup all of the routes 
        """
        
        # This has to be here for nasty circular dependency reasons
        # setup_api and setup_pages import Akabo, so if the import
        # is at the top of the page bad things happen
        from flaskapp.routes import setup_api, setup_pages

        # Use the api creator
        # We pass forward self, because self is a flaskapp and we hook routes onto it
        setup_api(self)
        setup_pages(self)

