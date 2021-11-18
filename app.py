from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.utils import redirect
from surveys import satisfaction_survey as survey
app = Flask(__name__)

app.config['SECRET_KEY'] = 'Test_key'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# initialize a variable called responses to be an empty list. As people answer questions, you should store their answers in this list.
response = []

@app.route('/')
def home_page():
    response.clear()
    return render_template("home.html", survey = survey)


@app.route('/questions/<q_num>')
def questions_page(q_num):
    q_num = len(response)
    question = survey.questions[q_num].question
    answers = survey.questions [q_num].choices

    if (q_num == len(survey.questions)):
        return redirect ('/complete')
    if (q_num != len(survey.questions)):
        return render_template('questions.html', q_num = q_num, question = question, answers = answers)

@app.route('/test', methods = ['POST'])
def test_page():
    choice = request.form['answer']
    response.append(choice)
    if (len(response) == len(survey.questions)):
        return redirect ('/complete')
    if (len(response) != len(survey.questions)):
        return redirect ('/questions/<q_num>')

@app.route('/complete')
def complete_page():
    return render_template ('complete.html')