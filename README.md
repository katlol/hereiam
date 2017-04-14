# hereiam
## PoC HTTP server + database for [`whereami`](https://github.com/kootenpv/whereami)

## Usage:
 - Set `HASHING_KEY=...` in `.env`
 - Get the key for your username
  ```
  python3 -c "key='asdf';name='simone';from hashlib import sha384 as s;print(s(f'{name}{key}'.encode  ('utf-8')).hexdigest())"
  ```
  Or if running in the container
  ```
  python3 -c "name='simone';from os import environ as e;key=e['HASHING_KEY'];from hashlib import sha384 as s;print(s(f'{name}{key}'.encode('utf-8')).hexdigest())"
  ```
  - Cron to regularly execute `curl http://hereiam/position/simone/asdf/$(whereami predict)`
## Endpoints
 - `/positions` - Get everyone's latest positions
 - `/positions/<name>` - Get a person's historical positions
 - `/position/<name>` - Get a person's latest position
 - `/position/<name>/<token>/<position>` - Save position
