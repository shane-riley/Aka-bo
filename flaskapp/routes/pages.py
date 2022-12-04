import flask
from firebase_admin import auth 
from flaskapp import Akabo
from flaskapp.shared import *

# Add pages api routes
def setup_pages(app: Akabo):

    if TESTING_MODE:
        # Test page
        @app.route('/test')
        def test_page():
            """
            Main page route.
            """
            return flask.redirect("/s/test.html", code=302)

    # Main page
    @app.route('/')
    def index_page():
        """
        Main page route.
        """
        return flask.redirect("/s/index.html", code=302)

    # Login/newuser page
    @app.route('/login')
    def login_page():
        """
        Login page route.
        """
        return flask.redirect("/s/login.html", code=302)
        
    # Profile Page (redirect if not logged in)
    @app.route('/profilepage')
    @secure_route
    def profilepage_page():
        """
        Profile Page Route
        """
        return flask.redirect("/s/profilepage.html", code=302)

    # Matchmaking page (redirect if not logged in)
    @app.route('/matchmaking')
    @secure_route
    def usermod_page():
        """
        User modification page route.

        If not logged in, drop to login page
        """
        return flask.redirect("/s/matchmaking.html", code=302)

    # Game page (redirect if not logged in)
    @app.route('/game')
    @secure_route
    def game_page():
        """
        User game page route.

        If not logged in, drop to login page
        """
        return flask.redirect("/s/connect4.html", code=302)