from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return 'Hello from Gateway!'

@app.route('/items', methods=['GET'])
@app.route('/items/<string:item_id>', methods=['GET'])
def get_devices(item_id=None):
    if item_id:
        response = requests.get(f'http://invsys:5000/items/{item_id}')
    else:
        response = requests.get('http://invsys:5000/items')
    return Response(response.content, response.status_code)

@app.route('/items/<string:item_id>', methods=['DELETE'])
def delete_device(item_id):
    response = requests.delete(f'http://invsys:5000/items/{item_id}')
    return Response(response.content, response.status_code)

@app.route('/items', methods=['POST'])
def post_device():
    payload = request.get_json(force=True)
    response = requests.post('http://invsys:5000/items', json=payload)
    return Response(response.content, response.status_code)

@app.route('/items/<string:item_id>', methods=['PUT'])
def put_device(item_id):
    payload = request.get_json(force=True)
    response = requests.put(f'http://invsys:5000/items/{item_id}', json=payload)
    return Response(response.content, response.status_code)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
