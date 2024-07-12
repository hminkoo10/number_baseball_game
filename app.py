from flask import Flask, render_template, request, jsonify, session
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # 세션 키 설정

# 5자리의 랜덤 숫자 생성
def generate_random_number():
    return ''.join(random.sample('0123456789', 5))

# 숫자 야구 게임 로직
def check_guess(secret, guess):
    strike = sum(1 for s, g in zip(secret, guess) if s == g)
    ball = sum(1 for g in guess if g in secret) - strike
    return strike, ball

@app.route('/')
def index():
    if 'secret_number' not in session:
        session['secret_number'] = generate_random_number()
        session['guesses'] = []
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    guess = request.form['guess']
    if len(guess) != 5 or not guess.isdigit():
        return jsonify({'error': 'Invalid input. Please enter a 5-digit number.'})
    
    if len(set(guess)) != len(guess):
        return jsonify({'error': 'Invalid input. The number contains duplicate digits.'})

    secret_number = session.get('secret_number')
    strike, ball = check_guess(secret_number, guess)
    
    session['guesses'].append({'guess': guess, 'strike': strike, 'ball': ball})

    if strike == 5:
        response = {'result': 'win', 'message': 'Congratulations! You guessed the correct number!', 'guesses': session['guesses']}
        session.pop('secret_number')
        session.pop('guesses')
    else:
        response = {'result': 'continue', 'strike': strike, 'ball': ball, 'guesses': session['guesses']}
    
    return jsonify(response)

@app.route('/get_secret_number', methods=['GET'])
def get_secret_number():
    secret_number = session.get('secret_number', '')
    return jsonify({'secret_number': secret_number})

if __name__ == '__main__':
    app.run(debug=True)
