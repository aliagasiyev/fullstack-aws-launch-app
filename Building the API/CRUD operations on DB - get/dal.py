import shelve
from flask import g

# Testlərin gözlədiyi ilkin məlumat
DEFAULT_DEVICES = {
    "001": {"id": "001", "name": "Light bulb",      "location": "hall",    "status": "off"},
    "002": {"id": "002", "name": "Humidity_sensor", "location": "bedroom", "status": "on"},
    "003": {"id": "003", "name": "Humidifier",      "location": "bedroom", "status": "off"},
}

def pull_db():
    """Shelve DB-ni aç və Flask g üzərində cache et (qapatmırıq!)."""
    db_ = getattr(g, '_database', None)
    if db_ is None:
        # writeback=False daha stabil və sürətlidir
        db_ = g._database = shelve.open("storage", writeback=False)
    return db_

def _seed_if_empty():
    """DB boşdursa, DEFAULT_DEVICES ilə doldur."""
    db = pull_db()
    if len(list(db.keys())) == 0:
        for k, v in DEFAULT_DEVICES.items():
            db[k] = v
        db.sync()

def get():
    """Bütün cihazları dict kimi qaytar (DB-ni BAĞLAMADAN!)."""
    _seed_if_empty()
    db = pull_db()
    # Shelve obyektinin üzərində birbaşa iterasiya etmək əvəzinə keys() istifadə edirik
    return {k: db[k] for k in db.keys()}
