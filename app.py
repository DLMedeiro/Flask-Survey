from flask import Flask, render_template, request, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.utils import redirect
from surveys import satisfaction_survey as survey
app = Flask(__name__)

app.config['SECRET_KEY'] = 'Test_key'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# initialize a variable called responses to be an empty list. As people answer questions, you should store their answers in this list.

@app.route('/')
def home_page():
    session['response'] = []
    return render_template("home.html", survey = survey)


@app.route('/questions/<q_num>')
def questions_page(q_num):
    q_num = len(session['response'])
    question = survey.questions[q_num].question
    answers = survey.questions [q_num].choices

    if (q_num == len(survey.questions)):
        return redirect ('/complete')
    if (q_num != len(survey.questions)):
        return render_template('questions.html', q_num = q_num, question = question, answers = answers)

# Step Six: Protecting Questions
# Right now, your survey app might be buggy. Once people know the URL structure, it’s possible for them to manually go to /questions/3 before they’ve answered questions 1 and 2. They could also try to go to a question id that doesn’t exist, like /questions/7.

# To fix this problem, you can modify your view function for the question show page to look at the number in the URL and make sure it’s correct. If not, you should redirect the user to the correct URL.

# For example, if the user has answered one survey question, but then tries to manually enter /questions/4 in the URL bar, you should redirect them to /questions/1.

# Once they’ve answered all of the questions, trying to access any of the question pages should redirect them to the thank you page.

# Step Seven: Flash Messages
# Using flash, if the user does try to tinker with the URL and visit questions out of order, flash a message telling them they’re trying to access an invalid question as part of your redirect.

# ??? Did I fix this without realizing it? / Not sure how to implement or what is being asked with my current set up


@app.route('/test', methods = ['POST'])
def test_page():
    choice = request.form['answer']
    response_s = session['response']
    response_s.append(choice)
    session['response'] = response_s
    if (len(session['response']) == len(survey.questions)):
        return redirect ('/complete')
    if (len(session['response']) != len(survey.questions)):
        return redirect ('/questions/<q_num>')

@app.route('/complete')
def complete_page():
    return render_template ('complete.html')