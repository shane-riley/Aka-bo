import flask
from .__init__ import app

# Add pages api routes

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