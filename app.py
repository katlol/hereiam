import sanic
import time

import settings
import utils

app = sanic.Sanic()

historical = settings.db['historical']
live = settings.db['live']


@app.route('/position/<name:[a-z]+>')
async def position_get(request, name):
    data = live.find_one(name=name)
    data['seconds_ago'] = utils.timeago(data['time'])
    return sanic.response.json(data)


@app.route('/positions/<name:[a-z]+>')
async def positions_user(request, name):
    data = historical.find(name=name, order_by='-time', _limit=100)
    results = []
    for event in data:
        event['seconds_ago'] = utils.timeago(event['time'])
        results.append(event)

    return sanic.response.json(results)


@app.route('/positions')
async def positions(request):
    data = live.find(order_by='-time', _limit=100)
    results = []
    for event in data:
        event['seconds_ago'] = utils.timeago(event['time'])
        results.append(event)     
        
    return sanic.response.json(results)


@app.route('/position/<name:[a-z]+>/<token:[a-z0-9]+>/<position:[a-zA-Z0-9-_]+>')
async def position_set(request, name, token, position):
    if not utils.verify_token(name, token):
        return sanic.response.json({'status': 'error', 'message': 'invalid token'})
    
    data = {'name': name, 'position': position, 'time': int(time.time())}
    historical.insert(data)
    live.upsert(data, ['name'])

    return sanic.response.json({'status': 'ok', 'message': 'updated'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=settings.bind_port)
