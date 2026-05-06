import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from RSA import generate_rsa_pair, load_rsa_private, rsa_decrypt, rsa_encrypt, save_rsa_keys
from utils import write_data, read_text, read_encrypted


def generate_and_save_keys(lenght, public_pem, private_pem, symmetric_path):
    private_key, public_key = generate_rsa_pair()
    symmetric_key = os.urandom(lenght//8)
    save_rsa_keys(public_key, public_pem, private_key, private_pem)
    save_symmetric_key(symmetric_key, symmetric_path, public_key)

     
def save_symmetric_key(key, symmetric_path, public_key):
    with open(symmetric_path, 'wb') as key_file:
        key_file.write(rsa_encrypt(key, public_key))
     

def load_symmetric_key(symmetric_path, private_key):
    with open(symmetric_path, mode='rb') as key_file: 
        symmetric_key = key_file.read()
        return rsa_decrypt(symmetric_key, private_key)


def aes_encrypt(path_to_data, private_pem, symmetric_path, path_to_save):
    private_key = load_rsa_private(private_pem)
    padder = padding.PKCS7(128).padder()
    text = read_text(path_to_data)
    padded_text = padder.update(text)+padder.finalize()
    key = load_symmetric_key(symmetric_path, private_key)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    c_text = encryptor.update(padded_text) + encryptor.finalize()
    write_data(iv + c_text, path_to_save)
        

def aes_decrypt(path_to_data, private_pem, symmetric_path, path_to_save):
    iv, c_text = read_encrypted(path_to_data)
    key = load_symmetric_key(symmetric_path, load_rsa_private(private_pem))
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    dc_text = decryptor.update(c_text) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()

    write_data(unpadded_dc_text, path_to_save)
