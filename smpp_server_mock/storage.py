# coding=utf-8

import os
import shelve

from contextlib import contextmanager
from fcntl import flock, LOCK_SH, LOCK_EX, LOCK_UN

DATA_DIR = 'data'


def get_shelve_object(name, write=False):
    address = os.path.join(DATA_DIR, name)

    connection = shelve.open(address)

    try:
        yield connection
    finally:
        connection.close()


class ShelveObject(object):
    def __init__(self, name):
        self.address = os.path.join(DATA_DIR, name)
        self.connection = None

    def __get_connection(self):
        if self.connection is not None:
            return self.connection

        self.connection = shelve.open(self.address)
        return self.connection

    def close(self):
        self.connection.close()
        self.connection = None

    @contextmanager
    def get_connection(self):
        try:
            return self.__get_connection()
        finally:
            self.close()
