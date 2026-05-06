from AES import aes_decrypt, aes_encrypt, generate_and_save_keys

def main():
    generate_and_save_keys(128, "public.pem", "private.pem", "symmetric.bin")
    aes_encrypt("source_text.txt", "private.pem", "symmetric.bin", "encrypt.txt")
    aes_decrypt("encrypt.txt", "private.pem", "symmetric.bin", "decrypt.txt")


if __name__ == "__main__":
    main()
