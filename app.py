from curses import flash
from flask import Flask, render_template, request, redirect
# from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__, template_folder='templates')
app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.config['DEBUG_TB_ENABLED'] = True
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# toolbar = DebugToolbarExtension(app)

responses = []

@app.route('/')
def index():
    return render_template('survey.html', survey=satisfaction_survey)

@app.route('/questions/<int:question_index>', methods=['GET', 'POST'])
def show_question(question_index):
    total_questions = len(satisfaction_survey.questions)
    if len(responses) == total_questions:
        return redirect('/thankyou')
    
    if 0 <= question_index < total_questions:
        question = satisfaction_survey.questions[question_index]

        if request.method == 'POST':
            user_answer = request.form.get('choice')
            responses.append(user_answer)

            if question_index + 1 < total_questions:
                return redirect(f'/questions/{question_index + 1}')
            
            else:
                return redirect('/thankyou')
            
        return render_template('question.html', question=question)
    
    else:
        flash('Invalid question index. Redirected to the first question.')
        return redirect('/questions/0')

@app.route('/thankyou')
def thank_you():
    return 'Thank You!'

if __name__ == '__main__':
    app.run(debug=True)