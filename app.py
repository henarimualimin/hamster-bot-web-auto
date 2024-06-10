import os
from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, emit
import threading
import hamster

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_initdata', methods=['POST'])
def update_initdata():
    initdata = request.form['initdata']
    with open('initdata.txt', 'w') as file:
        file.write(initdata)
    return redirect('/')

@app.route('/start_bot', methods=['POST'])
def start_bot():
    auto_upgrade_energy = request.form['auto_upgrade_energy']
    auto_upgrade_multitap = request.form['auto_upgrade_multitap']
    auto_upgrade_passive = request.form['auto_upgrade_passive']
    lanjut_upgrade = request.form['lanjut_upgrade']
    cek_task_list = request.form['cek_task_list']
    ask_cipher = request.form['ask_cipher']
    cipher_text = request.form['cipher_text']

    bot_thread = threading.Thread(target=run_bot, args=(auto_upgrade_energy, auto_upgrade_multitap, auto_upgrade_passive, lanjut_upgrade, cek_task_list, ask_cipher, cipher_text))
    bot_thread.start()
    return redirect('/')

def run_bot(auto_upgrade_energy, auto_upgrade_multitap, auto_upgrade_passive, lanjut_upgrade, cek_task_list, ask_cipher, cipher_text):
    hamster.main(auto_upgrade_energy, auto_upgrade_multitap, auto_upgrade_passive, lanjut_upgrade, cek_task_list, ask_cipher, cipher_text)

@socketio.on('connect')
def test_connect():
    emit('log', {'data': 'Connected'}, broadcast=True)

def log_to_web(message):
    socketio.emit('log', {'data': message})

if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True)
