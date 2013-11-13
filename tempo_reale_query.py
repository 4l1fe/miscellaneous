from urllib import request as req
import requests
from requests.auth import HTTPBasicAuth

url = 'http://10.76.113.44/query/ta'
psw_mgr = req.HTTPPasswordMgrWithDefaultRealm()
psw_mgr.add_password(None, url, 'admin', 'admin')
auth = req.HTTPBasicAuthHandler(psw_mgr)
opener = req.build_opener(auth)
resp = opener.open(url)
for line in resp.readlines():
    print(line.decode('cp1251'), end='')


# resp = requests.get(url, auth=HTTPBasicAuth('admin', 'admin'))
# resp.encoding = 'cp1251'
# print(resp.text)