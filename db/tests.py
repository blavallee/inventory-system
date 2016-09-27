

def cleanup():
    try:
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
    from db import upc_table
    upc_table.UpcTable().insert([upc_table.UpcRecord("1234567", "Mon test", "", "generated")])


def test_delete_upc():
    from db import upc_table
    upc_table.UpcTable().delete(["1234567"])


cleanup()
test_get_upc()
test_add_upc()
test_delete_upc()
test_add_upc()
try:
    test_add_upc_twice()
except:
    pass

