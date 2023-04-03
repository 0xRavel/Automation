import base64
import errno
import os
from Crypto.Cipher import AES
from typing import List

class AESCipher:
    def __init__(self, key: str, iv: str):
        self.key = key
        self.iv = iv

    def encrypt(self, source: str) -> str:
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        padding = AES.block_size - len(source) % AES.block_size
        data = source + chr(padding) * padding
        return base64.b64encode(cipher.encrypt(data)).decode()

    def decrypt(self, source: str) -> str:
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        data = cipher.decrypt(base64.b64decode(source))
        padding = ord(data[-1])
        if data[-padding:] != chr(padding) * padding:
            raise ValueError("Invalid padding...")
        return data[:-padding].decode()

def makedir(directory: str) -> None:
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("[E] makedir")

def process_files(action: str, files: List[str], cipher: AESCipher) -> None:
    makedir(action)

    for filename in files:
        out_path = os.path.join(action, filename)
        with open(filename, 'r') as inf:
            data = inf.read()

        if action == "dec":
            data = data.replace('\n', '')
            decrypted_data = cipher.decrypt(data)
            with open(out_path, "w") as f:
                f.write(decrypted_data)
            print(f"Decrypted data have been written into '{out_path}'")
        elif action == "enc":
            encrypted_data = cipher.encrypt(data)
            with open(out_path, "w") as f:
                f.write(encrypted_data)
            print(f"Encrypted data have been written into '{out_path}'")

if __name__ == '__main__':
    action = input("Enter 'enc' to encrypt or 'dec' to decrypt: ")
    key = input("Enter secret key: ")
    iv = input("Enter iv value: ")
    files_input = input("Enter the file(s) you want to encrypt/decrypt (separated by commas): ")

    files = [file.strip() for file in files_input.split(',')]
    cipher = AESCipher(key, iv)
    process_files(action, files, cipher)