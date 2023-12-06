from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys, satisfaction_survey, personality_quiz

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def main_page():
    satisfaction_survey = surveys['satisfaction']
    personality_quiz =  surveys['personality']
    return render_template('mainpage.html',satisfaction_survey=satisfaction_survey,personality_quiz=personality_quiz)

@app.route('/', methods=['POST'])
def select_survey():
    if request.form.get('satisfaction',None):
        satisfaction_survey= surveys['satisfaction']
        title = satisfaction_survey.title
        instructions = satisfaction_survey.instructions
        return render_template('home.html', title=title, instructions=instructions, survey="satisfaction")
    if  request.form.get('personality',None):
        personality_quiz =  surveys['personality']
        title = personality_quiz.title
        instructions = personality_quiz.instructions
        return render_template('home.html', title=title, instructions=instructions, survey="personality")    


@app.route('/start',methods=['POST']) 
def empty_list():
    chosensurvey = request.form.get('choosensurvey', "")
    if satisfaction_survey:
        session['responses'] = []
        session['questions'] = []
        return redirect('/question/' + chosensurvey + '/0')
    
    if personality_quiz:
        session['responses'] = []
        session['questions'] = []
        return redirect('/question/' + chosensurvey + '/0')
 
@app.route('/question/<choosensurvey>/<int:index>')
def get_new_question(choosensurvey,index):
    if choosensurvey == "satisfaction":
        responses = session['responses']
        questions = session['questions']
        if len(responses) == len(satisfaction_survey.questions):
            return redirect('/complete/'+choosensurvey)
        if index == len(responses):
            question = satisfaction_survey.questions[index].question
            choices= satisfaction_survey.questions[index].choices
            text=satisfaction_survey.questions[index].allow_text
            questions.append(question)
            session['questions'] = questions
            return render_template('questions.html',question=question,choices=choices,text=text,index=index+1,choosensurvey=choosensurvey)
        if index > len(responses):
            flash('You are trying to access an invalid question')
            return redirect('/question/'+choosensurvey+'/'+ str(len(responses)))
        if index < len(responses):
            flash('Visit question in order')
            return redirect('/question/'+choosensurvey+'/'+ str(len(responses)))
    elif choosensurvey == "personality":
        responses= session['responses']
        questions = session['questions']
        if len(responses) == len(personality_quiz.questions):
            return redirect('/complete/'+choosensurvey)
        if index == len(responses):
            question = personality_quiz.questions[index].question
            choices= personality_quiz.questions[index].choices
            text=personality_quiz.questions[index].allow_text
            questions.append(question)
            session['questions'] = questions
            return render_template('questions.html',question=question,choices=choices,text=text,index=index+1,choosensurvey=choosensurvey)
        if index > len(responses):
            flash('You are trying to access an invalid question')
            return redirect('/question/'+choosensurvey+'/'+ str(len(responses)))
        if index < len(responses):
            flash('Visit question in order')
            return redirect('/question/'+choosensurvey+'/'+ str(len(responses)))
    return "Invalid Response"
    
@app.route('/answer/<choosensurvey>/<int:index>', methods=["POST"])
def post_choice(choosensurvey,index):
    chosensurvey = request.form.get('choosensurvey', "")
    if choosensurvey == "satisfaction":
        responses= session['responses']
        choice = request.form["choice"]
        text = request.form.get("text","")
        response ={'choice':choice,'text':text}
        responses.append(response)
        session['responses'] = responses
        if index < len(satisfaction_survey.questions):
            return redirect('/question/'+choosensurvey+'/'+ str(index))
        if index >= len(satisfaction_survey.questions):
            return redirect('/complete/'+choosensurvey)
    elif choosensurvey == "personality":
        responses= session['responses']
        choice = request.form["choice"]
        text = request.form.get("text","")
        response ={'choice':choice,'text':text}
        responses.append(response)
        session['responses']= responses
        if index < len(personality_quiz.questions):
            return redirect('/question/'+choosensurvey+'/'+ str(index))
        if index >= len(personality_quiz.questions):
            return redirect('/complete/'+choosensurvey)
    
@app.route('/complete/<choosensurvey>')
def survey_complete(choosensurvey):
    if choosensurvey == 'satisfaction':
        responses= session['responses']
        questions = session['questions']
        return render_template('result.html', responses=responses,questions=questions,choosensurvey=choosensurvey)
    elif choosensurvey == 'personality':
        responses= session['responses']
        questions = session['questions']
        return render_template('result.html',responses=responses,questions=questions,choosensurvey=choosensurvey)