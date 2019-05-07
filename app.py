import requests
from cryptography.fernet import Fernet
from collections import defaultdict
import json
import random
import pickle
from bs4 import BeautifulSoup

from flask import Flask, request
app = Flask(__name__)

dat = pickle.load(open('new.dat', 'rb'))

def updatedb():
    nd = {0: {}, 1: {}, 2: {}}
    for x in dat:
        if x.startswith('DV'):
            nd[2][x] = dat[x]
        elif x.startswith('CSC7@'):
            nd[2][x] = dat[x]
        elif x.startswith('CSC@'):
            nd[1][x] = dat[x]
        elif x.startswith('JCH'):
            nd[1][x] = dat[x]
        else:
            nd[0][x] = dat[x]
    return dict(nd)

@app.route('/getdb')
def senddbsample():
    new = updatedb()
    ndb = defaultdict(dict)
    minlen = min([len(new[0]), len(new[1]), len(new[2])])
    if minlen > 5:
        minlen = 5
    for x in new:
        for y in random.sample(new[x].keys(), minlen):
            ndb[x][y] = new[x][y]

    return json.dumps([ndb[0], ndb[1], ndb[2]])

@app.route('/v2/getdb')
def senddbsamplenew():
    new = updatedb()
    ndb = defaultdict(dict)
    minlen = min([len(new[0]), len(new[1]), len(new[2])])
    if minlen > 5:
        minlen = 5
    for x in new:
        for y in random.sample(new[x].keys(), minlen):
            ndb[x][y] = new[x][y]

    return json.dumps([ndb[0], ndb[1], ndb[2]])


@app.route('/v2/ver')
def version():
    return '1.2'
