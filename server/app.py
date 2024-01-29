from flask import Flask, request, jsonify, render_template, send_file, Response, make_response
import threading
from collections import defaultdict
from natsort import natsorted
import numbers
import re
import numpy as np
import math
import threading

# Our modules
import image
import gen

app = Flask(__name__,
    template_folder='../static',
    static_folder='../static')

def validate_args(keywords, args, url):
    for kw in keywords:
        if kw not in args:
            return error(f'{kw} not in args ({url})')
    return None

# Multiple simultaneous users
client_idx = 0
clients = dict()

# Server sent events
cv = threading.Condition()

def make_state():
    state = dict()

    state['imgs'] = []
    state['descs'] = []
    state['data'] = []
    state['update'] = False

    return state

# Home screen
@app.route('/')
def index():
    global clients, client_idx
    resp = make_response(render_template('index.html'))
    resp.set_cookie('client_idx', str(client_idx))
    clients[client_idx] = make_state()
    client_idx += 1
    return resp

# Server sent events (for history)
@app.route('/history')
def history():
    global clients
    my_client_idx = int(request.cookies.get('client_idx'))
    print(my_client_idx)
    def event_stream():
        while True:
            with cv:
                for client_idx, state in clients.items():
                    if client_idx != my_client_idx:
                        continue
                    if not state['update']:
                        continue
                    state['update'] = False
                    img_descs = list(zip(state['imgs'], state['descs']))
                    with app.app_context():
                        history = render_template('history.html', img_descs=img_descs)
                    data = ' '.join(line.strip() for line in history.splitlines())
                    msg = f'event: update\ndata: {data}\n\n'
                    yield msg
                cv.wait()
    return Response(event_stream(), mimetype="text/event-stream")

def get_fc(args, var=False):
    age_mu = float(args['age_mu'])
    age_sigma = float(args['age_sigma'])
    age = (float(args['age'])-age_mu)/age_sigma
    sex = int(args['sex'] == 'male')
    race = int(args['race'] == 'aa')
    n = int(10**float(args['number']))
    global clients
    my_client_idx = int(request.cookies.get('client_idx'))
    img_idx = len(clients[my_client_idx]['imgs'])
    is_var = 'var' if var else 'mean'
    if args['dataset'] == 'pnc':
        task = args['task']
        imgdat = gen.gen(n, age, sex, race, task, var=var)
        desc = f'{img_idx}. {task} {args["age"]}yo {args["sex"]} {args["race"]} [{is_var} {n} subjects]'
    elif args['dataset'] == 'bsnip':
        diag = int(args['diag'] == 'sz')
        imgdat = gen.gen_bsnip(n, age, sex, race, diag, var=var)
        desc = f'{img_idx}, {args["diag"]} {args["age"]}yo {args["sex"]} {args["race"]} [{is_var} {n} subjects]'
    bounds = [0, 30, 35, 49, 62, 120, 125, 156, 181, 199, 212, 221, 232, 236, 264]
    img = image.imshow(imgdat, bounds=bounds)
    clients[my_client_idx]['imgs'].append(img)
    clients[my_client_idx]['descs'].append(desc)
    clients[my_client_idx]['data'].append(imgdat)
    clients[my_client_idx]['update'] = True
    with cv:
        cv.notify_all()
    return render_template('image.html', img=img)

# Generated FC
@app.route('/generate', methods=['POST'])
def generate():
    args = request.form
    return get_fc(args)

# Generate FC Variance
@app.route('/generate-var', methods=['POST'])
def generate_var():
    args = request.form
    return get_fc(args, True)

# Difference of Scans
@app.route('/difference', methods=['POST'])
def difference():
    args = request.form
    global clients
    my_client_idx = int(request.cookies.get('client_idx'))
    data = clients[my_client_idx]['data']
    if len(data) == 0:
        return ''
    i1 = int(args['scan1'])
    i2 = int(args['scan2'])
    imgdat = data[i1]-data[i2]
    bounds = [0, 30, 35, 49, 62, 120, 125, 156, 181, 199, 212, 221, 232, 236, 264]
    img = image.imshow(imgdat, bounds=bounds)
    return render_template('image.html', img=img)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8010, debug=True, threaded=True)
