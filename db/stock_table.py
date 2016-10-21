__author__ = 'blavallee'


class StockRecord(object):
    """
    stock record manipulation
    """
    def __init__(self, sequence_id, upc, description, expiration, date_achat):
        self._sequence_id = sequence_id
        self._upc = upc
        self._description = description
        self._expiration = expiration
        self._date_achat = date_achat

    def sequence_id(self):
        return self._sequence_id

    def upc(self):
        return self._upc

    def description(self):
        return self._description

    def expiration(self):
        return self._expiration

    def date_achat(self):
        return self._date_achat

    def __str__(self):
        return u'"upc":"{0}","Description":"{1}"'.format(self._upc, self._description)


class StockRecordSet(object):

    def __init__(self):
        self._records = []

    def add(self, record):
        self._records.append(record)

    def to_json(self, skip_header=False):
        all_json = ''
        if not skip_header:
            all_json = '{"stocks":['
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


class StockTable(object):
    """
    stock table manipulation
    """

    def select(self, upcs_to_find=[]):
        records_set = StockRecordSet()
        import pymysql
        select_string = "SELECT sequence_id, upc, description, expiration, date_achat FROM stock"
        if upcs_to_find:
            upcs_list = ""
            for upc in upcs_to_find:
                if len(upcs_list) > 0:
                    upcs_list = "{}{}".format(upcs_list, ',')
                upcs_list = "{}{}{}{}".format(upcs_list, '"', str(upc), '"')
            select_string = "{} {}{}{}".format(select_string, "where upc in (", upcs_list, ')')

        conn = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user='root', passwd='', db='inventaire')
        cur = conn.cursor()
        cur.execute(select_string)
        for r in cur:
            records_set.add(StockRecord(r[0], r[1], r[2], r[3], r[4]))
        cur.close()
        conn.close()
        return records_set

    def insert(self, records_to_add=[]):
        import pymysql
        conn = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user='root', passwd='',
                               db='inventaire')
        for rec in records_to_add:
            insert_string = "INSERT INTO stock(upc,description,expiration,date_achat) VALUES ('{}','{}','{}','{}')".format(rec.upc(), rec.description(), rec.expiration(), rec.date_achat())
            cur = conn.cursor()
            cur.execute(insert_string)
        cur.close()
        conn.commit()
        conn.close()

    def delete(self, sequence_id_to_delete=[]):
        import pymysql
        delete_string = "DELETE FROM stock "
        if sequence_id_to_delete:
            number_list = ""
            for number in sequence_id_to_delete:
                if len(number_list) > 0:
                    number_list = "{}{}".format(number_list, ',')
                number_list = "{}{}{}{}".format(number_list, '"', str(number), '"')
            delete_string = "{} {}{}{}".format(delete_string, "WHERE sequence_id in (", number_list, ')')

        conn = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user='root', passwd='', db='inventaire')
        cur = conn.cursor()
        cur.execute(delete_string)
        cur.close()
        conn.commit()
        conn.close()


    def delete_upcs(self, upcs_to_delete=[]):
        import pymysql
        delete_string = "DELETE FROM stock "
        if upcs_to_delete:
            number_list = ""
            for number in upcs_to_delete:
                if len(number_list) > 0:
                    number_list = "{}{}".format(number_list, ',')
                number_list = "{}{}{}{}".format(number_list, '"', str(number), '"')
            delete_string = "{} {}{}{}".format(delete_string, "WHERE upc in (", number_list, ')')

        conn = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user='root', passwd='',
                               db='inventaire')
        cur = conn.cursor()
        cur.execute(delete_string)
        cur.close()
        conn.commit()
        conn.close()
