import sys
import os
import flask

# Make app
app = flask.Flask(__name__)

# Load backend
import flaskapp


# import debugpy
# print("Shane!!!")
#Fee free to change the secret and port number
# debugpy.listen(('localhost', 5678))
#The debug server has started and you can now use VS Code to attach to the application for debugging
# print("Google App Engine has started, ready to attach the debugger")
if __name__=='__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)