# Some helpful utilities to help reduce redundancy
import pandas


def save_to_file(items, file):
    """
    utility method for saving collection to file
    :param items:
    :param file:
    :return:
    """
    # save items to file
    with open(file, "a") as file:
        for item in items:
            file.write(f"{item}\n")


def read_file(file):
    """
    read file contents
    :param file:
    :return items:
    """
    # read items from file
    items = []

    with open(file, "r") as file:
        for item in file:
            items.append(item)

    return items


def read_csv_file(filepath):
    """
    read username and password from accounts file
    :param filepath:
    :return accounts:
    """

    columns = ['username', 'password', 'email', 'e_password']
    df = pandas.read_csv(filepath, header=None, names=columns, delimiter=':')

    credentials = [(x, y, z) for x, y, z in zip(df['username'], df['password'], df['email'])]

    return credentials
