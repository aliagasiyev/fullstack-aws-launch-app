from flask import Flask, request, jsonify
from marshmallow import Schema, fields, ValidationError, validates_schema

app = Flask(__name__)

# Dictionary to mimic the database
devices = {
    "001": {"id": "001", "name": "Light bulb", "location": "hall", "status": "off"},
    "002": {"id": "002", "name": "Humidity sensor", "location": "bedroom", "status": "on"},
    "003": {"id": "003", "name": "Humidifier", "location": "bedroom", "status": "off"}
}


# Define Marshmallow Schema for request and response validation
class DeviceSchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    location = fields.Str(required=True)
    status = fields.Str(required=True)

    # Use validates_schema for custom validation logic
    @validates_schema(pass_original=True)
    def validate_required_fields(self, data, original_data, **kwargs):
        # declare required fields
        required_fields = ["id", "name", "location", "status"]

        # only enforce this custom check for POST (PUT-də partial icazəlidir)
        if request and request.method == "POST":
            payload = original_data or {}
            missing = [f for f in required_fields if f not in payload]
            if missing:
                # Hər çatmayan sahə üçün standart marshmallow formatında mesaj qaytaraq
                raise ValidationError({f: ["Missing data for required field."] for f in missing})


device_schema = DeviceSchema()


@app.route('/items/<string:identifier>', methods=['GET', 'PUT', 'DELETE'])
def device(identifier):
    if request.method == 'GET':
        device_data = devices.get(identifier)
        if not device_data:
            return jsonify({'message': 'Device not found'}), 404
        return jsonify(device_data), 200

    elif request.method == 'PUT':
        try:
            args = device_schema.load(request.json, partial=True)
        except ValidationError as err:
            return jsonify(err.messages), 400

        if identifier not in devices:
            return jsonify({'message': 'Device not found'}), 404

        devices[identifier].update(args)
        return jsonify({"updated device": identifier}), 200

    elif request.method == 'DELETE':
        if identifier not in devices:
            return jsonify({'message': 'Device not found'}), 404
        del devices[identifier]
        return jsonify({'message': 'Device deleted'}), 200


@app.route('/items', methods=['GET', 'POST'])
def device_inventory():
    if request.method == 'GET':
        # TEST-in istədiyi format: {"items": { "001": {...}, "002": {...}, ... }}
        return jsonify({"items": devices}), 200

    elif request.method == 'POST':
        # Payload-ı valideyt et
        try:
            new_device = device_schema.load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400

        # id unikal olmalıdır
        if new_device["id"] in devices:
            return jsonify({"message": "Device already exists"}), 400

        # əlavə et və TEST-in istədiyi cavabı qaytar
        devices[new_device["id"]] = new_device
        return jsonify({"Posted a device": new_device}), 201



if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
