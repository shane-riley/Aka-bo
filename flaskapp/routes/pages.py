import flask
from firebase_admin import auth 
from flaskapp import Akabo

# Add pages api routes
def setup_pages(app: Akabo):

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
        
    # Profile Page
    @app.route('/profilepage')
    def profilepage_page():
        """
        Profile Page Route
        """
        return flask.redirect("/s/profilepage.html", code=302)

    # Usermod page (drop to login if not authorized)
    @app.route('/user/<string:username>')
    def usermod_page(username):
        """
        User modification page route.

        If not logged in, drop to login page
        """
        # TODO: Implement me
        return login_page()

    # Game page
    @app.route('/game')
    def game_page(game, ticket):
        """
        User game page route.

        If not logged in, drop to login page

        If gameid doesn't match with the user, return a 404
        """
        # TODO: Implement me
        return login_page()