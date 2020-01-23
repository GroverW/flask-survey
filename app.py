from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"


responses = []
title = surveys.satisfaction_survey.title

@app.route('/')
def base():
    instructions = surveys.satisfaction_survey.instructions
    return render_template('base.html', title=title, instructions=instructions)

@app.route('/questions/<int:id>')
def questions(id):
    question_obj = surveys.satisfaction_survey.questions[id]
    question = question_obj.question
    choices = question_obj.choices

    return render_template('question.html', title=title, instructions=question, choices=choices, id=(id+1))


@app.route('/answer', methods=['POST'])
def answers():
    next_question = request.form['next-id']
    responses.append(request.form['choice'])
    
    return redirect(f'/questions/{next_question}')

