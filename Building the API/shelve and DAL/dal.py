import shelve

devices = {
    "001": {
        "id": "001",
        "name": "Light bulb",
        "location": "hall",
        "status": "off"
    },
    "002": {
        "id": "002",
        "name": "Humidity_sensor",
        "location": "bedroom",
        "status": "on"
    },
    "003": {
        "id": "003",
        "name": "Humidifier",
        "location": "bedroom",
        "status": "off"
    }
}

# Initialize db with some data already in it
with shelve.open('storage') as db:
    # Populate the database db with data
    for key, value in devices.items():
        db[key] = value

# For checking: print everything from storage
if __name__ == '__main__':
    with shelve.open('storage') as db:
        for key, value in db.items():
            print(key, "=>", value)
