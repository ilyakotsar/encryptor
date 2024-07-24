import json
import os
import random
import string
from argon2 import PasswordHasher
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def encrypt_text(plaintext: str, key: bytes, iv: bytes) -> str:
    cipher = Cipher(algorithms.AES256(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    return b64encode(ciphertext).decode()


def decrypt_text(ciphertext: str, key: bytes, iv: bytes) -> str:
    ciphertext = b64decode(ciphertext)
    cipher = Cipher(algorithms.AES256(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded) + unpadder.finalize()
    return plaintext.decode()


def generate_dh_parameters(key_size: int) -> tuple[int, int]:
    g = random.choice((2, 5))
    parameters = dh.generate_parameters(generator=g, key_size=key_size)
    numbers = parameters.parameter_numbers()
    return numbers.g, numbers.p


def generate_private_key(p: int) -> int:
    length = len(str(p)) - random.randint(0, 10)
    digits = [random.choice(string.digits) for _ in range(length)]
    return int(''.join(digits))


def create_public_key(g: int, private_key: int, p: int) -> int:
    return pow(g, private_key, p)


def create_shared_key(public_key: int, private_key: int, p: int) -> int:
    return pow(public_key, private_key, p)


def create_encryption_key(
        time_cost: int,
        memory_cost: int,
        parallelism: int,
        password: str,
        salt: bytes,
    ) -> bytes:
    ph = PasswordHasher(
        time_cost=time_cost,
        memory_cost=memory_cost,
        parallelism=parallelism,
        hash_len=24,
    )
    hash = ph.hash(password, salt=salt)
    return hash.split('$')[5].encode()


def generate_salt() -> bytes:
    return os.urandom(16)


def generate_iv() -> bytes:
    return os.urandom(16)


def get_settings() -> dict:
    with open('settings.json') as f:
        return json.load(f)


def create_symm_config(settings: dict, salt: bytes, iv: bytes, ciphertext: str) -> str:
    config = [str(settings['argon2'][i]) for i in settings['argon2']]
    config.extend([b64encode(i).decode() for i in (salt, iv)])
    config.append(ciphertext)
    return '|'.join(config)


def symm_config_str_to_dict(config: str) -> dict:
    config_list = config.split('|')
    config_dict = {
        'time_cost': int(config_list[0]),
        'memory_cost': int(config_list[1]),
        'parallelism': int(config_list[2]),
        'salt': b64decode(config_list[3]),
        'iv': b64decode(config_list[4]),
        'ciphertext': config_list[5],
    }
    return config_dict


def create_asymm_config(g: int, p: int, public_key: int, salt: bytes) -> str:
    with open('settings.json') as f:
        settings = json.load(f)
    config = ['A']
    config.extend([str(i) for i in (g, p, public_key)])
    config.extend([str(settings['argon2'][i]) for i in settings['argon2']])
    config.append(b64encode(salt).decode())
    return '|'.join(config)


def confirm_asymm_config(config: dict, public_key: int) -> str:
    config['user'] = 'B'
    config['public_key'] = public_key
    config_list = []
    for i in config:
        if i == 'salt':
            config_list.append(b64encode(config[i]).decode())
        else:
            config_list.append(str(config[i]))
    return '|'.join(config_list)


def asymm_config_str_to_dict(config: str) -> dict:
    config_list = config.split('|')
    config_dict = {
        'user': config_list[0],
        'g': int(config_list[1]),
        'p': int(config_list[2]),
        'public_key': int(config_list[3]),
        'time_cost': int(config_list[4]),
        'memory_cost': int(config_list[5]),
        'parallelism': int(config_list[6]),
        'salt': b64decode(config_list[7]),
    }
    return config_dict


def create_asymm_msg_config(user: str, iv: bytes, ciphertext: str) -> str:
    if user == 'A':
        config = ['B']
    elif user == 'B':
        config = ['A']
    config.append(b64encode(iv).decode())
    config.append(ciphertext)
    return '|'.join(config) 


def asymm_msg_config_str_to_dict(config: str) -> dict:
    config_list = config.split('|')
    config_dict = {
        'user': config_list[0],
        'iv': b64decode(config_list[1]),
        'ciphertext': config_list[2],
    }
    return config_dict

