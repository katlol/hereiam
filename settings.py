import os, sys, time
import dataset
import traceback

db_url = os.getenv('DB_URL', 'postgres://postgres@postgres/postgres')
bind_port = os.getenv('BIND_PORT', 80)

debug = os.getenv('DEBUG') is not None

hashing_key = os.getenv('HASHING_KEY')
if not hashing_key or len(hashing_key) < 128:
    print('Set environment variable HASHING_KEY to be 128+ characters long.')
    sys.exit()


def connect_to_db(tries=0):
    print('Connecting to postgres, try ', tries)
    if tries > 10:
        sys.exit(1)
    try:
        db = dataset.connect(db_url)
        time.sleep(tries*1000*2)
    except:
        traceback.print_exc()
        connect_to_db(tries+1)
    print('Connected to postgres')
    return db

db = connect_to_db()