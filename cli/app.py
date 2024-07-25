import os
import sys

sys.path.append(os.path.abspath(os.pardir))

import encryptor
from getpass import getpass

print('Encryptor\n')
print('1. Symmetric\n2. Asymmetric')
encryption_number = input('\nNumber: ')
# Symmetric
if encryption_number == '1':
    message = input('\nMessage: ')
    password = getpass('\nPassword: ')
    action = input('\nEncrypt or decrypt? [E/d]: ')
    # Symmetric decrypt
    if action.lower() == 'd':
        config = encryptor.symm_config_str_to_dict(message)
        encryption_key = encryptor.create_encryption_key(
            config['time_cost'],
            config['memory_cost'],
            config['parallelism'],
            password,
            config['salt'],
        )
        plaintext = encryptor.decrypt_text(config['ciphertext'], encryption_key, config['iv'])
        print(f'\nPlaintext: {plaintext}')
    # Symmetric encrypt
    else:
        settings = encryptor.get_settings()
        salt = encryptor.generate_salt()
        encryption_key = encryptor.create_encryption_key(
            settings['argon2']['time_cost'],
            settings['argon2']['memory_cost'],
            settings['argon2']['parallelism'],
            password,
            salt,
        )
        iv = encryptor.generate_iv()
        ciphertext = encryptor.encrypt_text(message, encryption_key, iv)
        config = encryptor.create_symm_config(
            settings['argon2']['time_cost'],
            settings['argon2']['memory_cost'],
            settings['argon2']['parallelism'],
            salt,
            iv,
            ciphertext,
        )
        print(f'\nEncrypted message: {config}')
# Asymmetric
elif encryption_number == '2':
    print('\n1. Create room\n2. Confirm room\n3. Open room')
    action = input('\nNumber: ')
    # Create room
    if action == '1':
        settings = encryptor.get_settings()
        print('\nGenerating parameters...')
        g, p = encryptor.generate_dh_parameters(settings['dh']['key_size'])
        private_key = encryptor.generate_private_key(p)
        public_key = encryptor.create_public_key(g, private_key, p)
        salt = encryptor.generate_salt()
        config = encryptor.create_asymm_config(
            settings['argon2']['time_cost'],
            settings['argon2']['memory_cost'],
            settings['argon2']['parallelism'],
            g,
            p,
            public_key,
            salt,
        )
        print(f'\nPrivate key A: {private_key}')
        print(f'\nConfiguration A: {config}')
    # Confirm room
    elif action == '2':
        config = input('\nConfiguration A: ')
        config = encryptor.asymm_config_str_to_dict(config)
        private_key = encryptor.generate_private_key(config['p'])
        public_key = encryptor.create_public_key(config['g'], private_key, config['p'])
        config_b = encryptor.confirm_asymm_config(config, public_key)
        print(f'\nPrivate key B: {private_key}')
        print(f'\nConfiguration B: {config_b}')
    # Open room
    elif action == '3':
        config = input('\nInterlocutor configuration: ')
        config = encryptor.asymm_config_str_to_dict(config)
        private_key = int(getpass('\nPrivate key: '))
        shared_key = encryptor.create_shared_key(config['public_key'], private_key, config['p'])
        print('\nCreating encryption key...')
        encryption_key = encryptor.create_encryption_key(
            config['time_cost'],
            config['memory_cost'],
            config['parallelism'],
            str(shared_key),
            config['salt'],
        )
        while True:
            message = input('\nMessage: ')
            action = input('\nEncrypt or decrypt? [E/d]: ')
            # Asymmetric decrypt
            if action.lower() == 'd':
                config = encryptor.asymm_msg_config_str_to_dict(message)
                plaintext = encryptor.decrypt_text(config['ciphertext'], encryption_key, config['iv'])
                print(f'\n{config['user']}: {plaintext}')
            # Asymmetric encrypt
            else:
                iv = encryptor.generate_iv()
                ciphertext = encryptor.encrypt_text(message, encryption_key, iv)
                config = encryptor.create_asymm_msg_config(config['user'], iv, ciphertext)
                print(f'\nEncrypted message: {config}')
            add_msg = input('\nAdd message? [Y/n]: ')
            if add_msg.lower() == 'n':
                break
input('\nPress Enter to exit')
