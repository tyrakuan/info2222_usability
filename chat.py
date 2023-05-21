from imports import ssl, render_template, emit, request, Flask, SocketIO
from database import Database
from msg_database import MessageDatabase
from flask import redirect, url_for, session

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
def another_chat(username):
    role = session['role']  # Fetch role from session
    return render_template('chat.html', username=username, role=role)

@app.route('/chat/<username>')
def chat(username, role):
    message = request.form.get('message')

    # Create a dictionary to represent the message
    message_data = {
        'username': username,
        'message': message,
    }

    messages.append(message_data)

    with open('messages.txt', 'a') as f:
        f.write(f"{message_data['username']}: ({message_data['title']}): {message_data['message']}\n")

    # Emit the message to all connected clients
    socketio.emit('message', message_data)

    return redirect(url_for('chat', username=username, role=role))


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
    session['role'] = user.role
    return redirect(url_for('another_chat', username=username))


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
    # Send message to all clients
    print("MESSAGE SENT")
    socketio.emit('message', data, broadcast=True)

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
    