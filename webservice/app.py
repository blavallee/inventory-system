from flask import Flask
from flask import request
from db import upc_table
import json

app = Flask(__name__)

@app.route('/upc/<code>', methods=['GET', 'POST'])
def upc(code):
    if request.method == 'GET':
        return json.dumps(upc_table.UpcTable().execute())
    else:
        return "HA NON"
 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
