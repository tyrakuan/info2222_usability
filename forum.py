from imports import ssl, render_template, emit, request, Flask, SocketIO
from database import Database
from flask import redirect
import datetime

database = Database()

app = Flask(__name__)

# A list to store the questions
questions = []

# Main pages
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

# @app.route('/')
# def index():
#     return render_template('index.html', questions=questions)

# Login routines
@app.route('/login')
def login():
    return render_template('login.html', return_message="")

@app.post('/login')
def login_info():
    username = request.form['username']
    password = request.form['password']
    
    if not (cc := database.check_credentials((username, password)))[0]:
        return render_template('login.html', return_message=cc[1])
    
    user = database.check_database(username)
    # return chat(username, user.friend_list)

@app.route('/forum', methods=['POST'])
def post_question():
    username = request.form['username']
    question = request.form['question']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a dictionary to represent the question
    question_data = {
        'username': username,
        'question': question,
        'timestamp': timestamp
    }

    # Append the question to the list
    questions.append(question_data)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
