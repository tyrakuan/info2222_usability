from imports import ssl, render_template, emit, request, Flask, SocketIO, BeautifulSoup
from database import Database
from msg_database import MessageDatabase, Message
from flask import redirect, url_for, session, jsonify


database = Database()
message_database = MessageDatabase()
# messages = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Main pages
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

# Chat page
@app.route('/chat')
def another_chat():
    role = session['role']  # Fetch role from session
    username = session['username'] # Fetch username from session
    return render_template('chat.html', username=username, role=role)

@app.route('/post_message', methods=['POST'])
def chat():

    role = session['role']  # Fetch role from session
    username = session['username'] # Fetch username from session

    message = request.form.get('message_input')

    message_data = Message(username, message)

    message_database.add_message_to_database(message_data)

    # messages.append(message_data)

    # return redirect(url_for('forum', username=username, role=role, messages=message_database.get_messages()))
    return render_template('forum.html', username=username, role=role, messages=message_database.get_messages())
    # return render_template('forum.html')

# Forum
@app.route('/forum')
def view_forum():
    username = session['username'] # Fetch username from session
    return render_template('forum.html', username=username)

# Course guide
@app.route('/guide')
def course_guide():
    # table_contents = database.course_guide_table
    paragraph_content = database.course_guide_paragraph_content
    return render_template('guide.html', paragraph_content=paragraph_content)

@app.route('/save', methods=['POST'])
def save_guide():

    # Retrieve the paragraph contents from the request
    updated_paragraph_content = request.form.get('paragraph_content')

    # Update the stored contents
    database.update_course_guide(updated_paragraph_content)

    return render_template('guide.html', paragraph_content=updated_paragraph_content)

# Account
@app.route('/account')
def account_management():
    return render_template('account.html')

# User - only for admins
@app.route('/users')
def user_management():
    return render_template('users.html')

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
    session['role'] = user.role
    session['username'] = user.username
    return redirect(url_for('another_chat'))


# Register routines
@app.route('/register')
def register():
    return render_template('register.html', return_message="")

@app.post('/register')
def register_info():
    
    username = request.form['username']
    hash_pass = request.form['hashed_password']
    salt = request.form['salt']
    role = request.form['role']

    return database.add_to_database((username, hash_pass, salt, role))
    

# emit message
@socketio.on('message')
def handle_message(data):
    print('received message: ' + str(data))
    emit('message', data, broadcast=True)

# get salt from database and return to front end

@app.route('/salt/<username>', methods=['GET'])
def return_salt(username):
    
    if (user := database.check_database(username)) is not None:
        salt = user.salt
        
    else: salt = "invalid"
    
    # print(salt)
    return salt


if __name__ == '__main__':
    cert = 'certificates/0.0.0.0.pem'
    key = 'certificates/0.0.0.0-key.pem'

    app.run(debug=True)

    # socketio.run(app, host='0.0.0.0', port=8080, certfile=cert, keyfile=key)
    