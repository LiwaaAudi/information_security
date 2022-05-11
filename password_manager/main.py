import pandas as pd
import os
import hashlib
from cryptography.fernet import Fernet
import warnings


class PasswordManager:
    def __init__(self):
        self.users_data = pd.read_csv('users.csv')
        self.passwords = pd.read_csv('passwords.csv')
        self.logged_in = False
        self.username = None
        self.uuid = None

    def register(self):
        """
        Create a new user
        :return: None
        """
        print('================ Register ==================')
        username = input('Enter username: ')
        pwd = input('Enter password: ')
        conf_pwd = input("Confirm password: ")

        if conf_pwd == pwd:
            enc = conf_pwd.encode()
            hash1 = hashlib.md5(enc).hexdigest()

        else:
            print('Passwords do not match')
            return self.register()

        key = Fernet.generate_key()
        self.users_data = self.users_data.append(
            {
                'uuid': key,
                'username': username,
                'password': hash1,
            },
            ignore_index=True)
        self.users_data.to_csv('users.csv', index=False)

    def login(self):
        """
        Login to the application
        :return: None
        """
        username = input('Enter username: ')
        pwd = input('Enter password: ')
        auth = pwd.encode()
        auth_hash = hashlib.md5(auth).hexdigest()

        if username in self.users_data['username'].values:
            if auth_hash == self.users_data[self.users_data['username'] == username]['password'].values[0]:
                print('Login successful!')
                self.logged_in = True
                self.username = username
                self.uuid = self.users_data[self.users_data['username'] == username]['uuid'].values[0]

        else:
            print('Login failed!')
            print('''
            1. Register
            2. Login again
            3. Exit
            ''')
            choice = input('Enter your choice: ')
            if choice == '1':
                return self.register()
            elif choice == '2':
                return self.login()
            return exit()

    def add_password(self):
        """
        Add a new password
        :return: None
        """
        print('================ Add New Password ==================')
        website = input('Enter website: ')
        username = input('Enter username or email: ')
        pwd = input('Enter password: ')
        uuid = self.uuid
        encrypted = Fernet(uuid).encrypt(pwd.encode()).decode()
        self.passwords = self.passwords.append(
            {
                'uuid': uuid,
                'site': website,
                'username': username,
                'password': encrypted,
            },
            ignore_index=True)
        self.passwords.to_csv('passwords.csv', index=False)
        return register(self)

    def view_passwords(self):
        """
        View all passwords
        :return: None
        """
        print('================ View All Passwords ==================')
        if self.logged_in:
            df = self.passwords.loc[self.passwords['uuid'] == self.uuid]
            df['password'] = df['password'].apply(lambda x: Fernet(self.uuid).decrypt(x.encode()).decode())
            print(df[['site', 'username', 'password']])
            return register(self)
        else:
            print('You must be logged in to view passwords!')
            return self.login()


def create_csv():
    """
    Create a new csv files
    :return: None
    """
    users_exists = os.path.exists('users.csv')
    passwords_exists = os.path.exists('passwords.csv')
    if not users_exists and not passwords_exists:
        print('Creating new csv files')
        users_data = pd.DataFrame(columns=['uuid', 'username', 'password'])
        users_data.to_csv('users.csv', index=False)
        passwords_data = pd.DataFrame(columns=['uuid', 'site', 'user', 'password'])
        passwords_data.to_csv('passwords.csv', index=False)
    return None


def home():
    print("""
    Welcome to the password manager
    1. Register
    2. Login
    3. Exit
    """)


def register(pm):
    choice = input('Enter your choice: ')
    print("""
    1. Add new password
    2. View passwords
    3. View site password
    4. Exit
    """)
    if choice == '1':
        return pm.add_password()
    elif choice == '2':
        return pm.view_passwords()
    elif choice == '3':
        return pm.view_site_password()
    elif choice == '4':
        return exit()
    else:
        return register(pm)


def mainMenu(pm, choice):
    if choice == '1':
        pm.register()
        print('Registration successful!')
        print('Please login to continue')
        pm.login()
        register(pm)
        return
    elif choice == '2':
        pm.login()
        register(pm)
        return
    elif choice == '3':
        exit()


def main():
    warnings.simplefilter(action='ignore', category=FutureWarning)
    create_csv()
    pm = PasswordManager()
    home()
    choice = input('Enter your choice: ')
    mainMenu(pm, choice)


if __name__ == '__main__':
    main()
