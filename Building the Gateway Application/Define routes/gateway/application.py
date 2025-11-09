from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return 'Hello from Gateway!'

# GET /items and GET /items/<string:item_id>
@app.route('/items', methods=['GET'])
@app.route('/items/<string:item_id>', methods=['GET'])
def get_devices(item_id=None):
    return 'Hello from GET'

# DELETE /items/<string:item_id>
@app.route('/items/<string:item_id>', methods=['DELETE'])
def delete_device(item_id):
    return 'Hello from DELETE'

# POST /items
@app.route('/items', methods=['POST'])
def post_device():
    return 'Hello from POST'

# PUT /items/<string:item_id>
@app.route('/items/<string:item_id>', methods=['PUT'])
def put_device(item_id):
    return 'Hello from PUT'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
