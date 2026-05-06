import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from RSA import (
    generate_rsa_pair,
    load_rsa_private,
    rsa_decrypt,
    rsa_encrypt,
    save_rsa_keys,
)
from utils import write_data, read_text, read_encrypted


def generate_and_save_keys(lenght: int, public_pem: str, private_pem: str, symmetric_path: str):
    """
    Генерирует и сохраняет тройку ключей(симметричный и публичный + приватный для RSA)

    Аргументы:
        lenght: длина симметричного ключа
        public_pem: путь для сохранения публичного ключа
        private_pem: путь для сохранения приватного ключа
        symmetric_path: путь сохранения симметричного ключа
    """
    private_key, public_key = generate_rsa_pair()
    symmetric_key = os.urandom(lenght // 8)
    save_rsa_keys(public_key, public_pem, private_key, private_pem)
    save_symmetric_key(symmetric_key, symmetric_path, public_key)


def save_symmetric_key(key: bytes, symmetric_path: str, public_key: bytes):
    """
    Сохранение симметричного ключа в файл

    Аргументы:
        key: симметричный ключ
        symmetric_path: путь для сохранения симметричного ключа
        public_key: публичный ключ
    """
    with open(symmetric_path, "wb") as key_file:
        key_file.write(rsa_encrypt(key, public_key))


def load_symmetric_key(symmetric_path: str, private_key: bytes):
    """
    Считывает симметричный ключ из файла

    Аргументы:
        symmetric_path: путь к симметричному ключу
        private_key: приватный ключ
    """
    with open(symmetric_path, mode="rb") as key_file:
        symmetric_key = key_file.read()
        return rsa_decrypt(symmetric_key, private_key)


def aes_encrypt(path_to_data: str, private_pem: str, symmetric_path: str, path_to_save: str):
    """
    Шифрует данные с помощью AES

    Аргументы:
        path_to_data: путь к исходным данным
        private_pem: путь к приватному ключу
        symmetric_path: путь к симметричному ключу
        path_to_save: путь для сохранения зашифрованного текса
    """
    private_key = load_rsa_private(private_pem)
    padder = padding.PKCS7(128).padder()
    text = read_text(path_to_data)
    padded_text = padder.update(text) + padder.finalize()
    key = load_symmetric_key(symmetric_path, private_key)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    c_text = encryptor.update(padded_text) + encryptor.finalize()
    write_data(iv + c_text, path_to_save)


def aes_decrypt(path_to_data: str, private_pem: str, symmetric_path: str, path_to_save: str):
    """
    Расшифровывает данные с помощью AES

    Аргументы:
        path_to_data: путь к исходным данным
        private_pem: путь к приватному ключу
        symmetric_path: путь к симметричному ключу
        path_to_save: путь для сохранения расшифрованных данных
    """
    iv, c_text = read_encrypted(path_to_data)
    key = load_symmetric_key(symmetric_path, load_rsa_private(private_pem))
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    dc_text = decryptor.update(c_text) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()

    write_data(unpadded_dc_text, path_to_save)
