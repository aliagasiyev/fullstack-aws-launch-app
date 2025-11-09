import shelve
from flask import g


# This function creates a database if none has yet been created,
# or opens it if it's already there.
def pull_db():
    db_ = getattr(g, '_database', None)
    if db_ is None:
        # writeback=False daha sabitdir
        db_ = g._database = shelve.open("storage", writeback=False)
    return db_


# This function returns the entire dataset of devices as a dictionary
def get():
    db = pull_db()  # Shelf-i BAĞLAMIRIQ
    devices_ = {}
    for key in db.keys():
        devices_[key] = db[key]
    return devices_


# This function adds a new element to the datastore of devices
def post(args):
    db = pull_db()  # Shelf-i BAĞLAMIRIQ
    new_id = args.get("id")

    # Check if the id already exists in the shelf, and if so — return an error message
    if new_id in db:
        return {"message": "Device with this ID already exists"}

    # If the ID does not exist, add the new device
    db[new_id] = args
    db.sync()
    return {"Posted a device": args}


# A Dict of Dicts to define initial devices
devices = {
    "001": {"id": "001", "name": "Light bulb",      "location": "hall",    "status": "off"},
    "002": {"id": "002", "name": "Humidity_sensor", "location": "bedroom", "status": "on"},
    "003": {"id": "003", "name": "Humidifier",      "location": "bedroom", "status": "off"},
}

# Initialize db with some data already in it (seeding)
with shelve.open('storage') as db:
    for key, value in devices.items():
        if key not in db:
            db[key] = value
