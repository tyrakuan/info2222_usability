from imports import ssl, render_template, emit, request, Flask, SocketIO
from database import Database

database = Database()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# main pages

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

# login routines

@app.route('/login')
def login():
    return render_template('login.html', return_message="")

@app.post('/login')
def login_info():
    username = request.form['username']
    password = request.form['password']
    # salt = request.form['salt']
    
    return database.check_credentials((username, password))

# register routines

@app.route('/register')
def register():
    return render_template('register.html', return_message="")

@app.post('/register')
def register_info():
    
    username = request.form['username']
    hash_pass = request.form['hashed_password']
    salt = request.form['salt']

    return database.add_to_database((username, hash_pass, salt))
    

# emit message

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    emit('message', message, broadcast=True)


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
    cert_2 = 'certificates/127.0.0.1.pem'
    key_2 = 'certificates/127.0.0.1-key.pem'
    
    # context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # context.load_cert_chain(cert, key)
    socketio.run(app, host='0.0.0.0', port=8080, certfile=cert, keyfile=key)
