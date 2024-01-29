import pickle
import numpy as np

mygen = None
mygen_bsnip = None

def gen(n, age, sex, race, task='rest', var=False):
    global mygen
    if mygen is None:
        with open('data/vae_1000_z30_cov6_264_rank5.pkl', 'rb') as f:
            mygen = pickle.load(f)
    rest = int(task == 'rest')
    nback = int(task == 'nback')
    emoid = int(task == 'emoid')
    x = np.random.normal(loc=0, scale=1/mygen['inv_sigma'], size=(n, 30))
    y = np.concatenate([
        np.ones((n,1))*age,
        np.ones((n,1))*sex,
        np.ones((n,1))*race,
        np.ones((n,1))*rest,
        np.ones((n,1))*nback,
        np.ones((n,1))*emoid], axis=1)
    x = np.concatenate([x, y], axis=1)
    # Decode
    w3 = mygen['dec1_w']
    b3 = np.expand_dims(mygen['dec1_b'], 0)
    x = x @ w3 + b3
    # ReLU
    x[x < 0] = 0
    w4 = mygen['dec2_w']
    b4 = np.expand_dims(mygen['dec2_b'], 0)
    x = x @ w4 + b4
    x = x.reshape((n, 264, 5))
    x = np.einsum('ijk,ilk->ijl', x, x)
    # Clamp non-real values
    x[x > 1] = 1
    if var:
        x = np.var(x, axis=0)
    else:
        x = np.mean(x, axis=0)
    return x

def gen_bsnip(n, age, sex, race, sz, var=False):
    global mygen_bsnip
    if mygen_bsnip is None:
        with open('data/vae_bsnip_1000_z30_cov4_264_rank5.pkl', 'rb') as f:
            mygen_bsnip = pickle.load(f)
    x = np.random.normal(loc=0, scale=1/mygen_bsnip['inv_sigma'], size=(n, 30))
    y = np.concatenate([
        np.ones((n,1))*age,
        np.ones((n,1))*sex,
        np.ones((n,1))*race,
        np.ones((n,1))*sz], axis=1)
    x = np.concatenate([x, y], axis=1)
    # Decode
    w3 = mygen_bsnip['dec1_w']
    b3 = np.expand_dims(mygen_bsnip['dec1_b'], 0)
    x = x @ w3 + b3
    # ReLU
    x[x < 0] = 0
    w4 = mygen_bsnip['dec2_w']
    b4 = np.expand_dims(mygen_bsnip['dec2_b'], 0)
    x = x @ w4 + b4
    x = x.reshape((n, 264, 5))
    x = np.einsum('ijk,ilk->ijl', x, x)
    # Clamp non-real values
    x[x > 1] = 1
    if var:
        x = np.var(x, axis=0)
    else:
        x = np.mean(x, axis=0)
    return x

