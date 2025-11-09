from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return 'Hello from Gateway!'

@app.route('/items', methods=['GET'])
@app.route('/items/<string:item_id>', methods=['GET'])
def get_devices(item_id=None):
    # Forward the request to the relevant endpoint in invsys
    if item_id:
        response = requests.get(f'http://invsys:5000/items/{item_id}')
    else:
        response = requests.get('http://invsys:5000/items')

    # Forward the response back to the client
    return Response(response.content, status=response.status_code, content_type=response.headers.get('Content-Type'))

@app.route('/items/<string:item_id>', methods=['DELETE'])
def delete_device(item_id):
    return 'Hello from DELETE'

@app.route('/items', methods=['POST'])
def post_device():
    return 'Hello from POST'

@app.route('/items/<string:item_id>', methods=['PUT'])
def put_device(item_id):
    return 'Hello from PUT'

if __name__ == "__main__":
    app.run("0.0.0.0", port=5001, debug=True)
