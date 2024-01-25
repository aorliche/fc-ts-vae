import pickle
import numpy as np

mygen = None

def init():
    global mygen
    with open('data/mygen2.pkl', 'rb') as f:
        mygen = pickle.load(f)

def gen(n, age, sex, race, task='rest', var=False):
    if mygen is None:
        init()
    rest = int(task == 'rest')
    nback = int(task == 'nback')
    emoid = int(task == 'emoid')
    x = np.random.normal(loc=0, scale=1, size=(n, 10))
    y = np.concatenate([
        np.ones((n,1))*age,
        np.ones((n,1))*sex,
        np.ones((n,1))*(1-sex),
        np.ones((n,1))*race,
        np.ones((n,1))*(1-race),
        np.ones((n,1))*rest,
        np.ones((n,1))*nback,
        np.ones((n,1))*emoid], axis=1)
    x = np.concatenate([x, y], axis=1)
    w1 = mygen['gen_enc1_w']
    b1 = mygen['gen_enc1_bias']
    x = x @ w1 + b1
    # ReLU
    x[x < 0] = 0
    w2 = mygen['gen_enc2_w']
    b2 = mygen['gen_enc2_bias']
    x = x @ w2 + b2
    # AE Decode
    w3 = mygen['enc_dec1_w']
    b3 = mygen['enc_dec1_bias']
    x = x @ w3 + b3
    x = x.reshape((n, 264, 5))
    x = np.einsum('ijk,ilk->ijl', x, x)
    # Clamp non-real values
    for i in range(len(x)):
        mx = np.max(np.abs(x[i]))  
        if mx > 1:
            x[x > 1] = 1
            x[x < -1] = -1
    if var:
        x = np.var(x, axis=0)
    else:
        x = np.mean(x, axis=0)
    return x
