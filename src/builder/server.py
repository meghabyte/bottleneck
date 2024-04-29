import numpy as np
import io
import socketio
from aiohttp import web
import random
from collections import defaultdict
from experiment import BuilderExperiment
from urllib.parse import parse_qs

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


experiments = defaultdict(list)

async def index(request):
    path = request._message.path[2:]
    parsed = parse_qs(path)
    if('username' in parsed):
        username = parsed['username'][0]
        experiments[username].append(BuilderExperiment(username))
        with open("index.html") as f:
            return web.Response(text=f.read(), content_type='text/html')
    else:
        username = "invalid"
        experiments[username].append(BuilderExperiment(username))
        with open("invalid.html") as f:
            return web.Response(text=f.read(), content_type='text/html')



@sio.on('finish')
async def finish(sid, message):
    print("Finishing 1 image..")
    username = message["username"]
    colors = message["colors"]
    shapes = message["shapes"]
    positions = message["positions"]
    experiment = experiments[username][-1]
    experiment.add_steps(colors, shapes, positions)
    next_instruction_text, next_instruction_num = experiment.get_next_instruction()
    print(next_instruction_text)
    if(not next_instruction_text):
        # save user experiment log
        experiment.save()
        await sio.emit('endExperiment', {}, to=sid)
    else:
        await sio.emit('startNextImage', {"instruction_text":next_instruction_text, "instruction_num":next_instruction_num}, to=sid)
    
    
@sio.on('start')
async def start(sid, message):
    print("start")
    username = message["username"]
    print(username)
    print(experiments[username])
    experiment = experiments[username][-1]
    next_instruction_text, next_instruction_num = experiment.get_next_instruction()
    await sio.emit('startNextImage', {"instruction_text":next_instruction_text, "instruction_num":next_instruction_num}, to=sid)


app.router.add_get('/', index)
app.router.add_static('/static/',
                          path='./static/',
                          name='static')
if __name__ == '__main__':
    web.run_app(app, port=8000)
    

