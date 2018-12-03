import csv
import os

STATIC_PATH = os.path.join(os.path.dirname(__file__), '../static/')
FILENAME = '{}-data.csv'


def create_file(org):
    """
    Create or override a file in the storage

    :param org: name of organisation
    """
    open(STATIC_PATH + FILENAME.format(org), 'w').close()


def exist_file(org):
    """
    Check if a file exists in the storage

    :param org: name of organisation
    :return: True is exists, else False
    """
    return os.path.isfile(STATIC_PATH + FILENAME.format(org))


def save(org, data):
    """
    Saves data to a csv file in the storage

    :param org: name of organisation
    :param data: a list of list representing respectively rows and columns to write
    """
    with open(STATIC_PATH + FILENAME.format(org), mode='a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)


def load(org):
    """
    Load csv file data in the storage

    :param org: name of organisation
    :return: loaded data
    """
    with open(STATIC_PATH + FILENAME.format(org), mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        data = list(csv_reader)

    return data