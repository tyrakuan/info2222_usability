from imports import ssl, render_template, emit, request, Flask, SocketIO
from database import Database
from msg_database import MessageDatabase
from flask import redirect, url_for

database = Database()
# messages = MessageDatabase()
messages = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Main pages
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

# Chat page
@app.route('/chat/<username>')
def another_chat(username, role):
    return render_template('chat.html', username=username, role=role)

@app.route('/chat/<username>', methods=['POST'])
def chat(username, role):
    # title = request.form.get('title')
    message = request.form.get('message')

    # Create a dictionary to represent the message
    message_data = {
        'username': username,
        'message': message,
    }

    messages.append(message_data)

    # # Append the question to the list
    # messages.add_message_to_database(message_data)
    # messages.read_from_database()

    with open('messages.txt', 'a') as f:
        f.write(f"{message_data['username']}: ({message_data['title']}): {message_data['message']}\n")

    # Emit the message to all connected clients
    socketio.emit('message', message_data)

    return redirect(url_for('chat', username=username, role=role))  # it's better to redirect after POST


# Course guide
@app.route('/guide')
def course_guide():
    return render_template('guide.html')

# Account - html does not exist yet
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
    return another_chat(username, user.role)

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
    # Send message to all clients, except the sender
    socketio.emit('message', data, broadcast=True, include_self=False)

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
