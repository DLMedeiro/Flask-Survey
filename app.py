import os
from dotenv import load_dotenv

from flask import Flask, render_template, request, session, redirect
# from flask_debugtoolbar import DebugToolbarExtension
# This (below) keeps appearing..?
# from werkzeug.utils import redirect
from surveys import satisfaction_survey as survey

load_dotenv()
secret_key = os.getenv('SECRET_KEY')
app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key
# debug = DebugToolbarExtension(app)
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# initialize a variable called responses to be an empty list. As people answer questions, you should store their answers in this list.

@app.route('/')
def home_page():
    # When home page is loaded, response list is emptied for the session
    session['response'] = []
    # Template renders the statisfaction survey imported from surveys.py
    return render_template("home.html", survey = survey)


# Initiated when the submit button is clicked on the home page
# Works but not sure why
@app.route('/questions/<q>')
def questions_page(q):
    q_num = len(session['response'])
    question = survey.questions[q_num].question
    answers = survey.questions [q_num].choices
    print(q)
    if (q_num == len(survey.questions)):
        return redirect ('/complete')
    if (q_num != len(survey.questions)):
        return render_template('questions.html', q_num = q_num, question = question, answers = answers)


# Updates the session response list until the length matches the length of the questions avaialble
# Repetitive?
@app.route('/response', methods = ['POST'])
def response_page():
    choice = request.form['answer']
    response_s = session['response']
    response_s.append(choice)
    session['response'] = response_s

    if (len(session['response']) == len(survey.questions)):
        return redirect ('/complete')
    if (len(session['response']) != len(survey.questions)):
        return redirect ('/questions/0')

# Shows copmletion message if all questions are answered and logged into the responses list
@app.route('/complete')
def complete_page():
    return render_template ('complete.html')