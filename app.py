from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_socketio import SocketIO, emit
import hamster
import threading
import sys

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_initdata', methods=['POST'])
def update_initdata():
    content = request.form.get('content')
    with open('initdata.txt', 'w') as f:
        f.write(content)
    return jsonify({"message": "initdata.txt updated successfully"})

@app.route('/start_bot', methods=['POST'])
def start_bot():
    auto_upgrade_energy = request.form.get('auto_upgrade_energy', 'n')
    auto_upgrade_multitap = request.form.get('auto_upgrade_multitap', 'n')
    auto_upgrade_passive = request.form.get('auto_upgrade_passive', 'n')
    lanjut_upgrade = request.form.get('lanjut_upgrade', 'n')
    cek_task_list = request.form.get('cek_task_list', 'n')
    ask_cipher = request.form.get('ask_cipher', 'n')
    cipher_text = request.form.get('cipher_text', '')

    # Jalankan fungsi main di thread terpisah
    threading.Thread(target=run_bot, args=(auto_upgrade_energy, auto_upgrade_multitap, auto_upgrade_passive, lanjut_upgrade, cek_task_list, ask_cipher, cipher_text)).start()

    return redirect(url_for('index'))

def run_bot(auto_upgrade_energy, auto_upgrade_multitap, auto_upgrade_passive, lanjut_upgrade, cek_task_list, ask_cipher, cipher_text):
    # Redirect stdout to capture print statements
    sys.stdout = EmittingStream(lambda message: socketio.emit('log', {'data': message}))
    hamster.main(auto_upgrade_energy, auto_upgrade_multitap, auto_upgrade_passive, lanjut_upgrade, cek_task_list, ask_cipher, cipher_text)

class EmittingStream:
    def __init__(self, callback):
        self.callback = callback

    def write(self, message):
        if message.strip():
            self.callback(message)

    def flush(self):
        pass

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5004)