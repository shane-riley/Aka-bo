import flask
from .__init__ import app
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

    # Login page
    @app.route('/login')
    def login_page():
        """
        Login page route.
        """
        return flask.redirect("/s/login.html", code=302)

    # Newuser page
    @app.route('/newuser')
    def newuser_page():
        """
        User creation page route.
        """
        return flask.redirect("/s/newuser.html", code=302)
        
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

    # Matchmaking (drop to login if not authorized)
    @app.route('/matchmaking/<string:game>/<string:ticket>')
    def matchmaking_page(game, ticket):
        """
        User matchmaking page route.

        If not logged in, drop to login page

        If ticket doesn't match with the user, return a 404
        """
        # TODO: Implement me
        return login_page()

    # Game (drop to login if not authorized)
    @app.route('/matchmaking/<string:game>/<string:gameid>')
    def game_page(game, ticket):
        """
        User game page route.

        If not logged in, drop to login page

        If gameid doesn't match with the user, return a 404
        """
        # TODO: Implement me
        return login_page()

# M2
# @app.route('/email')
# def root():
#     return flask.redirect("/s/email-password.html", code=302)

# @app.route('/send', methods=['POST', 'GET'])
# def checkUser():
#     # return flask.redirect("/s/WelcomePage.html", code=302)
#     # result = flask.request.args
#     result = flask.request.form

#     id_token = result['token']
#     # id_token = id_token['value']
#     # id_token = id_token[2]
#     # return flask.render_template('index.html')
#     # id_token comes from the client app (shown above)
#     try:
#         auth.verify_id_token(id_token)
#         return flask.redirect("/s/WelcomePage.html", code=302)
#     except:
#         return flask.redirect("/s/index.html", code=302)
#     # return flask.redirect("/s/WelcomePage.html", code=302)

# @app.route('/connect4')
# def game():
#     return flask.redirect("/s/connect4.html", code=302)