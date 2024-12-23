from cryptography.fernet import Fernet
import os
def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
def load_key():
    if not os.path.exists("key.key"):
        write_key()
    with open("key.key", "rb") as key_file:
        key = key_file.read()
        try:
            Fernet(key)
        except ValueError:
            print("Invalid key detected. Regenerating the key.")
            write_key()
            key = load_key()
        return key
key = load_key()
fer = Fernet(key)
def view():
    try:
        with open("passwords.txt", "r") as f:
            for line in f.readlines():
                if '|' in line:
                    user, passw = line.strip().split("|")
                    decrypted_passw = fer.decrypt(passw.encode()).decode()
                    print(f"User: {user} | Password: {decrypted_passw}")
    except FileNotFoundError:
        print("No passwords saved yet.")
    except Exception as e:
        print(f"An error occurred: {e}")
def add():
    name = input("Account Name: ")
    pwd = input("Password: ")
    with open("passwords.txt", "a") as f:
        encrypted_pwd = fer.encrypt(pwd.encode()).decode()
        f.write(f"{name}|{encrypted_pwd}\n")
while True:
    mode = input("Would you like to add a new password or view existing passwords (view, add), or press z to quit: ").lower()
    if mode == "z":
        break
    elif mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("Invalid input. Please try again.")