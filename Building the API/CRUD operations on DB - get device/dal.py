import shelve
from flask import g


# Open (or create) the shelve DB and cache it on Flask g.
def pull_db():
    db_ = getattr(g, '_database', None)
    if db_ is None:
        db_ = g._database = shelve.open("storage", writeback=False)
    return db_


# Return entire dataset as a dict (DO NOT close the shelf)
def get():
    db = pull_db()
    return {key: db[key] for key in db.keys()}


# Add a new element to the datastore (DO NOT close the shelf)
def post(args):
    db = pull_db()
    db[args['id']] = args
    db.sync()
    return db[args['id']]


# Retrieve an item by its identifier; return None if not found
def get_device(identifier):
    db = pull_db()
    if identifier not in db:
        return None
    return db[identifier]


# Initial seed (only for first run)
devices = {
    "001": {"id": "001", "name": "Light bulb",      "location": "hall",    "status": "off"},
    "002": {"id": "002", "name": "Humidity_sensor", "location": "bedroom", "status": "on"},
    "003": {"id": "003", "name": "Humidifier",      "location": "bedroom", "status": "off"},
}

# Seed storage if keys missing (run-time safe)
with shelve.open('storage', writeback=False) as db:
    for key, value in devices.items():
        if key not in db:
            db[key] = value
