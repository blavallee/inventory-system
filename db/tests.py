

def cleanup():
    try:
        from db import stock_table
        stock_table.StockTable().delete_upcs(["1234567"])
        from db import upc_table
        upc_table.UpcTable().delete(["1234567"])
    except:
        pass


def test_get_upc():
    from db import upc_table
    print upc_table.UpcTable().select().to_json()
    upc_table = upc_table.UpcTable()
    print upc_table.select(['0060410074978']).to_json()
    print upc_table.select(['0060410074978']).to_json(True)


def test_add_upc():
    from db import upc_table
    upc_table.UpcTable().insert([upc_table.UpcRecord("1234567", "Mon test", "", "generated")])


def test_add_upc_twice():
    test_delete_upc()

    test_add_upc()
    try:
        test_add_upc()
        raise
    except:
        pass

def test_delete_upc():
    from db import upc_table
    upc_table.UpcTable().delete(["1234567"])

def test_get_stock():
    from db import stock_table
    print stock_table.StockTable().select().to_json()
    stock_table = stock_table.StockTable()
    print stock_table.select(['1234567']).to_json()
    print stock_table.select(['1234567']).to_json(True)


def test_add_stock():
    from db import stock_table
    stock_table.StockTable().insert([stock_table.StockRecord(None, "1234567", "Mon test", "2016-09-09", "2016-09-09")])

def test_delete_stock():
    from db import stock_table
    stock_table.StockTable().delete(["1234567"])


cleanup()
test_get_upc()
test_add_upc()
test_delete_upc()
test_add_upc_twice()

test_add_stock()
test_get_stock()
test_delete_stock()

cleanup()
