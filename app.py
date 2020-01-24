from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# TITLE = surveys.satisfaction_survey.title
# NUM_QUESTIONS = len(surveys.satisfaction_survey.questions)


@app.route('/')
def base():
    """Main page to tell user to start survey"""

    # instructions = surveys.satisfaction_survey.instructions
    return render_template(
        'base.html', surveys=surveys)


@app.route('/start', methods=["POST"])
def init_responses():
    """Direct here to reset variables"""
    session["survey"] = request.form['choice']
    session["responses"] = []
    session["current_question"] = 0
    return redirect("/questions/0")


@app.route('/questions/<int:id>')
def questions(id):
    """Show question form, redirect if user is screwing around"""

    if session.get("current_question") == None:
        return redirect('/')

    survey = surveys[session["survey"]]

    # Already done with survey -> thanks page
    current_question = session['current_question']
    if current_question >= len(survey.questions):
        return redirect('/Thanks')

    # Inserting incorrect question during survey -> correct question
    if id != current_question:
        flash("Stop! Hey! Listen! You did the wrong question!")
        return redirect(f'/questions/{current_question}')

    question_obj = survey.questions[id]
    question = question_obj.question
    choices = question_obj.choices

    return render_template(
        'question.html',
        instructions=question,
        choices=choices)


@app.route('/Thanks')
def thank():
    """Thanks page"""

    return "<p style='font-size: 260'>THANK YOU</p>"


@app.route('/answer', methods=['POST'])
def answers():
    """Increment questions and redirect"""

    # somehow got here without starting session
    if session.get("responses") == None:
        return redirect('/')

    survey = surveys[session["survey"]]
    next_question = session.get("current_question", -1) + 1

    # only add answer if next_question wasn't set above
    if next_question > 0:
        responses = session["responses"]
        responses.append(request.form['choice'])
        session["responses"] = responses

    session["current_question"] = next_question

    # thanks when done, next question otherwise
    next_page = (
        f'/questions/{next_question}'
        if int(next_question) < len(survey.questions)
        else '/Thanks')

    return redirect(next_page)
