from imports import ssl, render_template, emit, request, Flask, SocketIO
from database import Database
from flask import redirect
import datetime

database = Database()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Store messages in a list
messages = []

# Main pages
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

# Chat page
@app.route('/chat/<username>')
def chat(username, role):
    return render_template('chat.html', username=username, role=role)

@app.post('/chat/<username>')
def chat_info(username):
    title = request.form['title']
    message = request.form['message']

    # Create a dictionary to represent the question
    message_data = {
        'username': username,
        'title': title,
        'message': message,
    }

    # Append the question to the list
    messages.append(message_data)

    return render_template('chat.html', username=username, role=role)

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
    return chat(username, user.role)

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
def handle_message(message):
    username = request.args.get('username')
    
    print('received message: ', message)
    emit('message', message, broadcast=True)
    
@socketio.on('publicKey')
def handle_public_key(publicKey):
    emit('publicKey', publicKey, broadcast=True)

# get salt from database and return to front end

@app.route('/salt/<username>', methods=['GET'])
def return_salt(username):
    
    if (user := database.check_database(username)) is not None:
        salt = user.salt
        
    else: salt = "invalid"
    
    # print(salt)
    return salt


if __name__ == '__main__':
    app.run(debug=True)
    # cert = 'certificates/0.0.0.0.pem'
    # key = 'certificates/0.0.0.0-key.pem'
    # # cert_2 = 'certificates/127.0.0.1.pem'
    # # key_2 = 'certificates/127.0.0.1-key.pem'
    
    # socketio.run(app, host='0.0.0.0', port=8080, certfile=cert, keyfile=key)
