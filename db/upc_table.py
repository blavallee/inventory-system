__author__ = 'blavallee'


from enum import Enum


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

    def number(self):
        return self._number

    def description(self):
        return self._description

    def size_weight(self):
        return self._size_weight

    def source(self):
        return self._source

    def __str__(self):
        return u'"Id":"{0}","Description":"{1}"'.format(self._number, self._description)


class UpcRecordSet(object):

    def __init__(self):
        self._records = []

    def add(self, record):
        self._records.append(record)

    def to_json(self, skip_header=False):
        all_json = ''
        if not skip_header:
            all_json = '{"records":['
        for rec in self._records:
            all_json = '{}{}{}{}'.format(all_json, '{', str(rec), '},')
        if not skip_header:
            all_json = '{}{}'.format(all_json, ']}')
        return all_json

    def is_empty(self):
        if len(self._records) == 0:
            return True
        else:
            return False


class UpcTable(object):
    """
    upc table manipulation
    """

    def select(self, numbers_to_find=[]):
        records_set = UpcRecordSet()
        import pymysql
        select_string = "SELECT number, description, size_weight, source FROM upc"
        if numbers_to_find:
            number_list = ""
            for number in numbers_to_find:
                if len(number_list) > 0:
                    number_list = "{}{}".format(number_list, ',')
                number_list = "{}{}{}{}".format(number_list, '"', str(number), '"')
            select_string = "{} {}{}{}".format(select_string, "where number in (", number_list, ')')

        conn = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user='root', passwd='tomate23', db='inventaire')
        cur = conn.cursor()
        cur.execute(select_string)
        for r in cur:
            records_set.add(UpcRecord(r[0], r[1], r[2], r[3]))
        cur.close()
        conn.close()
        return records_set


    def insert(self, records_to_add=[]):
        import pymysql
        conn = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user='root', passwd='tomate23',
                               db='inventaire')
        for rec in records_to_add:
            insert_string = "INSERT INTO upc(number,description,size_weight,source) VALUES ('{}','{}','{}','{}')".format(rec.number(), rec.description(), rec.size_weight(), rec.source())
            cur = conn.cursor()
            cur.execute(insert_string)
        cur.close()
        conn.commit()
        conn.close()

    def delete(self, numbers_to_delete=[]):
        import pymysql
        delete_string = "DELETE FROM upc "
        if numbers_to_delete:
            number_list = ""
            for number in numbers_to_delete:
                if len(number_list) > 0:
                    number_list = "{}{}".format(number_list, ',')
                number_list = "{}{}{}{}".format(number_list, '"', str(number), '"')
            delete_string = "{} {}{}{}".format(delete_string, "WHERE number in (", number_list, ')')

        conn = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user='root', passwd='tomate23', db='inventaire')
        cur = conn.cursor()
        cur.execute(delete_string)
        cur.close()
        conn.commit()
        conn.close()
