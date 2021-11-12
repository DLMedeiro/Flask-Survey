from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Testing'
debug = DebugToolbarExtension(app)

# initialize a variable called responses to be an empty list. As people answer questions, you should store their answers in this list.
response = []

@app.route('/')
def home_page():
    # return f"<h1>Hello Testing</h1>"
    return render_template('test.html')