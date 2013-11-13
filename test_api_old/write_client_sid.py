import argparse
import dbm
import sys


sys.path.append('')

from sbis_root import *

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--client', action='store', dest='client', type=str, required=True, metavar='')
parser.add_argument('-psw', '--password', action='store', dest='password', type=str, required=True, metavar='')
parser.add_argument('-f', '--file_sid', action='store', dest='file_sid', type=str, required=True, metavar='')
result = parser.parse_args()

try:
    sid = САП.Аутентифицировать(result.client, result.password)
    error = b''
except RuntimeError as e:
    sid = b''
    error = e

file_sid = dbm.open(result.file_sid, 'c')

if sid:
    sid = sid.encode()
file_sid['sid'] = sid

if error:
    error = str(error).encode()
file_sid['error'] = error
file_sid['old_password'] = result.password.encode()

file_sid.close()