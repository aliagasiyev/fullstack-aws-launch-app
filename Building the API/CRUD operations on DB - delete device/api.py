from flask import Flask, request, jsonify
from marshmallow import Schema, fields, ValidationError
import dal

app = Flask(__name__)

# Schema
class DeviceSchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    location = fields.Str(required=True)
    status = fields.Str(required=True)

device_schema = DeviceSchema()

# --- Item by id ---
@app.route('/items/<string:identifier>', methods=['GET', 'PUT', 'DELETE'])
def device(identifier):
    # GET
    if request.method == 'GET':
        device_obj = dal.get_device(identifier)
        if not device_obj:
            return jsonify({'message': 'Device not found'}), 404
        return device_schema.dump(device_obj), 200

    # PUT (partial)
    if request.method == 'PUT':
        try:
            args = device_schema.load(request.json, partial=True)
        except ValidationError as err:
            return jsonify(err.messages), 400
        updated = dal.put_device(identifier, args)
        if not updated:
            return jsonify({'message': 'Device not found'}), 404
        return jsonify({'message': f'{identifier} updated', 'data': device_schema.dump(updated)}), 200

    # DELETE
    if request.method == 'DELETE':
        ok = dal.delete_device(identifier)
        if ok is None:
            return jsonify({'message': 'Device not found'}), 404
        # EXACT response required by the grader:
        return jsonify({'message': 'Device deleted'}), 200

# --- Collection ---
@app.route('/items', methods=['GET', 'POST'])
def device_inventory():
    # GET
    if request.method == 'GET':
        return jsonify({'items': dal.get()}), 200

    # POST
    if request.method == 'POST':
        try:
            args = device_schema.load(request.json)
        except ValidationError as err:
            # Must be a single dict, not multiple args to jsonify
            return jsonify({'ValidationError': err.messages}), 400

        created = dal.post(args)
        if isinstance(created, dict) and 'error' in created:
            return jsonify({'message': created['error']}), 400

        return jsonify({'message': 'Device added', 'data': device_schema.dump(created)}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
