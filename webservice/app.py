from flask import Flask
from flask import request
from db import upc_table
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
            return ('{number, description and source is mandatory}', 404, [])
        size_weight = ""
        if "size_weight" in request.json:
            size_weight = request.json["size_weight"]

        upc_table.UpcTable().insert([upc_table.UpcRecord(request.json["number"], request.json["description"],
                                                         size_weight, request.json["source"])])

        return ('{}', 201, [])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
