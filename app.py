from flask import Flask, render_template, request, redirect
from surveys import satisfaction_survey

app = Flask(__name__, template_folder='templates')
app.config["TEMPLATES_AUTO_RELAOD"] = True

responses = []

@app.route('/')
def index():
    return render_template('survey.html', survey=satisfaction_survey)

@app.route('/questions/<int:question_index>', methods=['GET', 'POST'])
def show_question(question_index):
    if 0 <= question_index < len(satisfaction_survey.questions):
        question = satisfaction_survey.questions[question_index]

        if request.method == 'POST':
            user_answer = request.form['choice']
            responses.append(user_answer)

            if question_index + 1 < len(satisfaction_survey.questions):
                return redirect(f'/questions/{question_index + 1}')
            else:
                return redirect('/thankyou')
        
        return render_template('question.html', question=question)
    else:
        return 'Question not found', 404


if __name__ == '__main__':
    app.run(debug=True)