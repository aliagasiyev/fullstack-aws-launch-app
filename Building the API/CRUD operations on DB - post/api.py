from flask import Flask, request, jsonify
from marshmallow import Schema, fields, ValidationError, validates_schema
import dal  # DAL qatını modul səviyyəsində import edirik

app = Flask(__name__)

# ---- Schema ----
class DeviceSchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    location = fields.Str(required=True)
    status = fields.Str(required=True)

    # POST üçün bütün sahələr tələb olunur (PUT-də partial ola bilər)
    @validates_schema(pass_original=True)
    def validate_required_fields(self, data, original_data, **kwargs):
        if request and request.method == "POST":
            payload = original_data or {}
            required = ["id", "name", "location", "status"]
            missing = [f for f in required if f not in payload]
            if missing:
                # marshmallow-un gözlədiyi format
                raise ValidationError({f: ["Missing data for required field."] for f in missing})

device_schema = DeviceSchema()

# ---- YALNIZ bu route lazımdır bu mərhələdə ----
@app.route('/items', methods=['GET', 'POST'])
def device_inventory():
    if request.method == 'GET':
        # Test bunu gözləyir: {"items": { "001": {...}, ... }}
        items = dal.get()
        return jsonify({"items": items}), 200

    # POST logic
    try:
        new_device = device_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # DAL vasitəsilə shelve DB-yə yazırıq (devices dict YOX!)
    db = dal.pull_db()          # DB-ni BAĞLAMIRIQ
    if new_device["id"] in db:
        return jsonify({'message': 'Device with this ID already exists'}), 400

    db[new_device["id"]] = new_device
    db.sync()
    return jsonify({"Posted a device": new_device}), 201


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
