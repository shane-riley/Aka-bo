from flaskapp import Akabo

# Make app (runs setup code in constructor)
app = Akabo(__name__)

if __name__=='__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)