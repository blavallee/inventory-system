from flask import Flask
from flask import request
from db import upc_table
from db import stock_table
import json

app = Flask(__name__)


@app.route('/upcs', methods=['POST'])
@app.route('/upcs/<code>', methods=['GET'])
def upcs(code=None):
    if request.method == 'GET':
        upcRecordSet = upc_table.UpcTable().select([code])
        if upcRecordSet.is_empty():
            return ('{}', 404, [])
        return upcRecordSet.to_json(True)
    else:
        # Read the json
        if code:
            return ('{Invalid request}', 404, [])
        if 'number' not in request.json or 'source' not in request.json or 'description' not in request.json:
            return ('{number, description and source are mandatory}', 404, [])
        size_weight = ""
        if "size_weight" in request.json:
            size_weight = request.json["size_weight"]

        upc_table.UpcTable().insert([upc_table.UpcRecord(request.json["number"], request.json["description"],
                                                         size_weight, request.json["source"])])

        return ('{}', 201, [])

@app.route('/stock', methods=['POST'])
@app.route('/stock/<code>', methods=['GET'])
def stock(code=None):
    if request.method == 'GET':
        stockRecordSet = stock_table.StockTable().select([code])
        if stockRecordSet.is_empty():
            return ('{}', 404, [])
        return stockRecordSet.to_json(True)
    else:
        # Read the json
        if code:
            return ('{Invalid request}', 404, [])
        if 'upc' not in request.json or 'description' not in request.json or 'expiration' not in request.json or 'date_achat' not in request.json:
            return ('{upc, description, expiration and date_achat are mandatory}', 404, [])

        stock_table.StockTable().insert([stock_table.StockRecord(None, request.json["upc"], request.json["description"],
                                                                 request.json["expiration"], request.json["date_achat"])])

        return ('{}', 201, [])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
