from flask import Flask, render_template, request, redirect, session, url_for
import random
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

LEADERBOARD_FILE = 'leaderboard.json'

QUIZ_DATA = [
    {
        "question": "What planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Venus", "Jupiter"],
        "answer": "Mars"
    },
    {
        "question": "What gas do plants absorb?",
        "options": ["Oxygen", "Carbon Dioxide", "Hydrogen", "Nitrogen"],
        "answer": "Carbon Dioxide"
    },
    {
        "question": "Who was the first president of the USA?",
        "options": ["George Washington", "John Adams", "Abraham Lincoln", "Thomas Jefferson"],
        "answer": "George Washington"
    },
    {
        "question": "In which year did World War II end?",
        "options": ["1945", "1939", "1918", "1950"],
        "answer": "1945"
    },
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "answer": "Paris"
    },
    {
        "question": "What is the hardest natural substance on Earth?",
        "options": ["Gold", "Iron", "Diamond", "Quartz"],
        "answer": "Diamond"
    },
    {
        "question": "Which ocean is the largest?",
        "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
        "answer": "Pacific Ocean"
    },
    {
        "question": "Who invented the telephone?",
        "options": ["Albert Einstein", "Alexander Graham Bell", "Isaac Newton", "Nikola Tesla"],
        "answer": "Alexander Graham Bell"
    },
    {
        "question": "What is the boiling point of water?",
        "options": ["90°C", "100°C", "110°C", "120°C"],
        "answer": "100°C"
    },
    {
        "question": "Which country is known as the Land of the Rising Sun?",
        "options": ["India", "Australia", "Japan", "China"],
        "answer": "Japan"
    },
    {
        "question": "What language has the most native speakers worldwide?",
        "options": ["English", "Mandarin Chinese", "Spanish", "Hindi"],
        "answer": "Mandarin Chinese"
    },
    {
        "question": "How many continents are there on Earth?",
        "options": ["5", "6", "7", "8"],
        "answer": "7"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Pablo Picasso", "Vincent van Gogh", "Leonardo da Vinci", "Claude Monet"],
        "answer": "Leonardo da Vinci"
    },
    {
        "question": "What is the smallest prime number?",
        "options": ["1", "2", "3", "5"],
        "answer": "2"
    },
    {
        "question": "Which programming language is primarily used for web development?",
        "options": ["Python", "Java", "HTML", "C++"],
        "answer": "HTML"
    }
]


def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'r') as f:
            return json.load(f)
    return []

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard, f)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['score'] = 0
        session['questions'] = random.sample(QUIZ_DATA, 10)

        session['current_index'] = 0
        return redirect(url_for('quiz'))
    return render_template('login.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'username' not in session:
        return redirect(url_for('login'))

    index = session['current_index']
    questions = session['questions']

    if request.method == 'POST':
        selected = request.form.get('option')
        correct = questions[index - 1]['answer']
        if selected == correct:
            session['score'] += 10
        else:
            session['score'] -= 5

    if index >= len(questions):
        return redirect(url_for('result'))

    session['current_index'] += 1
    question = questions[index]
    return render_template('quiz.html', question=question, index=index + 1, total=len(questions))

@app.route('/result')
def result():
    leaderboard = load_leaderboard()
    leaderboard.append({"name": session['username'], "score": session['score']})
    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)[:5]
    save_leaderboard(leaderboard)
    return render_template('result.html', score=session['score'])

@app.route('/leaderboard')
def leaderboard():
    board = load_leaderboard()
    return render_template('leaderboard.html', leaderboard=board)

if __name__ == '__main__':
    app.run(debug=True)
