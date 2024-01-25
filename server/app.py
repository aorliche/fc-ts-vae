from flask import Flask, request, jsonify, render_template, send_file, Response, make_response
import threading
from collections import defaultdict
from natsort import natsorted
import numbers
import re
import numpy as np
import math

# Our modules
import image
import gen

app = Flask(__name__,
    template_folder='../static',
    static_folder='../static')

def error(msg):
    return jsonify({'err': msg})

def validate_args(keywords, args, url):
    for kw in keywords:
        if kw not in args:
            return error(f'{kw} not in args ({url})')
    return None

# Multiple simultaneous users
client_idx = 0
clients = dict()

def make_state():
    state = dict()

    # Which content pane is visible
    state['imgs'] = []
    state['descriptions'] = []

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

def get_fc(args, var=False):
    age = int(args['age'])
    sex = int(args['sex'] == 'male')
    race = int(args['race'] == 'aa')
    task = args['task']
    n = int(10**float(args['number']))
    imgdat = gen.gen(n, age, sex, race, task, var=var)
    bounds = [0, 30, 35, 49, 62, 120, 125, 156, 181, 199, 212, 221, 232, 236, 264]
    img = image.imshow(imgdat, bounds=bounds)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8009, debug=True, threaded=True)
