import os
import sys

sys.path.append(os.path.abspath(os.pardir))

import encryptor
import json
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


@app.get('/')
def home():
    return render_template('home.html')


@app.route('/symmetric', methods=['GET', 'POST'])
def symmetric():
    if request.method == 'POST':
        data = json.loads(request.data)
        if 'encrypt' in data:
            plaintext = data['plaintext']
            time_cost = int(data['time_cost'])
            memory_cost = int(data['memory_cost'])
            parallelism = int(data['parallelism'])
            password = data['password']
            salt = encryptor.generate_salt()
            encryption_key = encryptor.create_encryption_key(
                time_cost,
                memory_cost,
                parallelism,
                password,
                salt,
            )
            iv = encryptor.generate_iv()
            ciphertext = encryptor.encrypt_text(plaintext, encryption_key, iv)
            encrypted_message = encryptor.create_symm_config(
                time_cost,
                memory_cost,
                parallelism,
                salt,
                iv,
                ciphertext,
            )
            return jsonify({'encrypted_message': encrypted_message})
        elif 'decrypt' in data:
            encrypted_message = data['encrypted_message']
            password = data['password']
            config = encryptor.symm_config_str_to_dict(encrypted_message)
            encryption_key = encryptor.create_encryption_key(
                config['time_cost'],
                config['memory_cost'],
                config['parallelism'],
                password,
                config['salt'],
            )
            plaintext = encryptor.decrypt_text(config['ciphertext'], encryption_key, config['iv'])
            return jsonify({
                'plaintext': plaintext,
                'time_cost': config['time_cost'],
                'memory_cost': config['memory_cost'],
                'parallelism': config['parallelism'],
            })
    return render_template('symmetric.html')


@app.route('/asymmetric', methods=['GET', 'POST'])
def asymmetric():
    return render_template('asymmetric.html')

