from flask import Flask, request, jsonify
from marshmallow import Schema, fields, ValidationError, validates_schema
import dal

app = Flask(__name__)


# ---- Schema ----
class DeviceSchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    location = fields.Str(required=True)
    status = fields.Str(required=True)

    # POST üçün bütün sahələr tələb olunur; PUT partial ola bilər
    @validates_schema(pass_original=True)
    def validate_required_fields(self, data, original_data, **kwargs):
        if request and request.method == "POST":
            payload = original_data or {}
            required = ["id", "name", "location", "status"]
            missing = [f for f in required if f not in payload]
            if missing:
                raise ValidationError({f: ["Missing data for required field."] for f in missing})


device_schema = DeviceSchema()


# ---- Single item: GET / PUT / DELETE ----
@app.route('/items/<string:identifier>', methods=['GET', 'PUT', 'DELETE'])
def device(identifier):
    if request.method == 'GET':
        item = dal.get_device(identifier)
        if item is None:
            return jsonify({'message': 'Device not found'}), 404
        return jsonify(item), 200

    elif request.method == 'PUT':
        try:
            args = device_schema.load(request.json, partial=True)  # partial update allowed
        except ValidationError as err:
            return jsonify(err.messages), 400

        updated = dal.put_device(identifier, args)
        if updated is None:
            return jsonify({'message': 'Device not found'}), 404
        return jsonify({"updated device": identifier}), 200

    elif request.method == 'DELETE':
        db = dal.pull_db()
        if identifier not in db:
            return jsonify({'message': 'Device not found'}), 404
        del db[identifier]
        db.sync()
        return jsonify({'message': 'Device deleted'}), 200


# ---- Collection: GET / POST ----
@app.route('/items', methods=['GET', 'POST'])
def device_inventory():
    if request.method == 'GET':
        devices_dict = dal.get()  # {"id": {...}, ...}
        return jsonify({"items": devices_dict}), 200

    # POST
    try:
        args = device_schema.load(request.json)
    except ValidationError as err:
        # düzgün format: sadəcə err.messages JSON-u
        return jsonify(err.messages), 400

    db = dal.pull_db()
    if args["id"] in db:
        return jsonify({'message': 'Device with this ID already exists'}), 400

    db[args["id"]] = args
    db.sync()
    return jsonify({"Posted a device": args}), 201


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
