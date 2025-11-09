import shelve
from flask import g


# Open (or create) the shelve DB and cache it on Flask g (do NOT close it here).
def pull_db():
    db_ = getattr(g, '_database', None)
    if db_ is None:
        db_ = g._database = shelve.open("storage", writeback=False)
    return db_


# Return entire dataset as a dict (do NOT close the shelf).
def get():
    db = pull_db()
    return {key: db[key] for key in db.keys()}


# Add a new element to the datastore (do NOT close the shelf).
def post(args):
    db = pull_db()
    db[args['id']] = args
    db.sync()
    return db[args['id']]


# Retrieve an item by its identifier; return None if not found.
def get_device(identifier):
    db = pull_db()
    if identifier not in db:
        return None
    return db[identifier]


# Update an item by id with provided args (partial update). Return updated item or None if not found.
def put_device(identifier, args):
    db = pull_db()
    if identifier not in db:
        return None

    device = dict(db[identifier])
    # partial update: yalnız göndərilən sahələri dəyiş
    for field, value in args.items():
        if value is not None:
            device[field] = value

    db[identifier] = device
    db.sync()
    return db[identifier]


# A Dict of Dicts to define initial devices (seed)
devices_seed = {
    "001": {"id": "001", "name": "Light bulb",      "location": "hall",    "status": "off"},
    "002": {"id": "002", "name": "Humidity_sensor", "location": "bedroom", "status": "on"},
    "003": {"id": "003", "name": "Humidifier",      "location": "bedroom", "status": "off"},
}

# Seed storage if empty / missing keys (safe at import time)
with shelve.open('storage', writeback=False) as _db:
    for k, v in devices_seed.items():
        if k not in _db:
            _db[k] = v
