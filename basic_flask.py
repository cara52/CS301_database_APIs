from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Server Works!'
    
@app.route('/greet')
def say_hello():
    return 'Hello from Server'

#adding variables
@app.route('/user/<username>')
def show_user(username):
    #returns the username
    return 'Username: %s' % username
