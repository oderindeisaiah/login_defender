import hashlib
import os
import getpass
import time

USERS_FILE = "users.db"
MAX_ATTEMPTS = 3
LOCK_TIME = 30  # seconds

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def load_users() -> dict:
    if not os.path.exists(USERS_FILE):
        return {}
    users = {}
    with open(USERS_FILE, "r") as file:
        for line in file:
            username, pwd_hash = line.strip().split("|")
            users[username] = pwd_hash
    return users

def save_users(users: dict):
    with open(USERS_FILE, "w") as file:
        for user, pwd_hash in users.items():
            file.write(f"{user}|{pwd_hash}\n")

def register():
    print("=== Register New User ===")
    username = input("Enter username: ").strip()
    password = getpass.getpass("Enter password: ")
    confirm = getpass.getpass("Confirm password: ")
    if password != confirm:
        print("Passwords do not match.")
        return

    users = load_users()
    users[username] = hash_password(password)
    save_users(users)
    print("User registered successfully!")

def login():
    print("=== Login ===")
    users = load_users()
    username = input("Username: ").strip()
    if username not in users:
        print("User not found!")
        return

    attempts = 0
    while attempts < MAX_ATTEMPTS:
        password = getpass.getpass("Password: ")
        if hash_password(password) == users[username]:
            print("Access granted.")
            return
        attempts += 1
        print(f"Wrong password. Attempts left: {MAX_ATTEMPTS - attempts}")

    print(f"Too many failed attempts. Locked for {LOCK_TIME} seconds.")
    time.sleep(LOCK_TIME)
    print("Try again.")

def main():
    print("=== Login Defender ===")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()