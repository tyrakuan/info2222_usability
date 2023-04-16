from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('./chat.html')

@socketio.on('chat message')
def handle_message(message):
    emit('chat message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, port=8080)


