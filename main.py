import flask
import json
from flask import request
import verifyUser
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth 

cred = credentials.Certificate("/home/clericgray/Aka-bo/graycs1520-firebase-adminsdk-iddjw-aa2d6f0631.json")
default_app = firebase_admin.initialize_app(cred)
app = flask.Flask(__name__)

@app.route('/')
def root():
    return flask.redirect("/s/email-password.html", code=302)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)


@app.route('/send', methods=['POST', 'GET'])
def checkUser():
    # return flask.redirect("/s/WelcomePage.html", code=302)
    # result = flask.request.json
    result = flask.request.form

    id_token = result['token']
    # id_token = id_token['value']
    # id_token = id_token[2]
    # return flask.render_template('index.html')
    # id_token comes from the client app (shown above)
    try:
        auth.verify_id_token(id_token)
        return flask.redirect("/s/WelcomePage.html", code=302)
    except:
        return flask.redirect("/s/index.html", code=302)
    # return flask.redirect("/s/WelcomePage.html", code=302)


    # except ValueError:
    #     print("Oops!  That was no valid number.  Try again...")
    # except InvalidTokenError:
    #     print("That token was invalid")
    # except ExpiredIdTokenError:
    #     print("That token is expired")
    # except RevokedIdTokenError:
    #     print("That token is revoked")
    # except CertificateFetchError:
    #     print("Was unable to verify token")
    # except UserDisabledError:
    #     print("User is disabled")