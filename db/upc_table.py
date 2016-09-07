__author__ = 'blavallee'

import pymysql
from enum import Enum
import json

class UpcSource(Enum):
    UPC_DB = "upc_db"
    GENERATED = "generated"
    REAL = "real"

class UpcRecord(object):
    """
    upc record manipulation
    """
    def __init__(self, number, description, size_weight, source):
        self._number = number
        self._description = description
        self._size_weight = size_weight
        self._source = source

    def __str__(self):
        return u"{ Id:0}, Description:{1}".format(self._number, self._description)

class UpcTable(object):
    """
    upc table manipulation
    """

    def __init__(self):
        self._records = []

    def execute(self):
        select_string = "SELECT number, description, size_weight, source FROM upc"

        conn = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user='root', passwd='tomate23', db='inventaire')
        cur = conn.cursor()
        cur.execute(select_string)
        for r in cur:
            self._records.append(UpcRecord(r[0], r[1], r[2], r[3]))
        cur.close()
        conn.close()

        return self._records

    def __str__(self):
        ret = ""
        for d in json.JSONEncoder().iterencode(self._records):
            ret = ret + d
        return ret
