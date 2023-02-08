import time
import pandas
from user import TwitterUser


def read_file(filepath):
    """
    read username and password from accounts file
    :param filepath:
    :return accounts:
    """

    columns = ['username', 'password', 'email', 'e_password']
    df = pandas.read_csv(filepath, header=None, names=columns, delimiter=':')

    credentials = [(x, y, z) for x, y, z in zip(df['username'], df['password'], df['email'])]

    return credentials


def main():
    """
    code starts here
    :return:
    """
    # keep a list of users already messaged
    already_messaged = []
    locked_dm = []

    accounts = read_file('accounts')

    for account in accounts:
        username, password, email = account

        user = TwitterUser(username, password, email)

        user.login()

        time.sleep(4)

        user.logout()

        time.sleep(5)

    # create a file for users that have been DMed
    with open("users_already_dm.txt", "x") as file:
        for user in already_messaged:
            file.write(f"{user}\n")


if __name__ == "__main__":
    # main()
    accounts = read_file('accounts')
    for account in accounts:
        print(account)
