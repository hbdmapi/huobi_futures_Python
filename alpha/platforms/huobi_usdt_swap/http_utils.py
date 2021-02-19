import requests
from urllib import parse
from alpha.utils import logger
import json
from datetime import datetime
import hmac
import base64
from hashlib import sha256

def get(host:str, path:str, params:dict = None)->json:
    try:
        url = 'http://{}{}'.format(host, path)
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        res = requests.get(url, params=params, headers = headers)
        data = res.json()
        return data
    except Exception as e:
        logger.error(e)
    return None


def __get_post_url_suffix(access_key:str, secret_key:str, host:str, path:str)->str:
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    timestamp = parse.quote(timestamp)
    suffix = 'AccessKeyId={}&SignatureMethod=HmacSHA256&SignatureVersion=2&Timestamp={}'.format(access_key, timestamp)
    payload = 'POST\n{}\n{}\n{}'.format(host, path, suffix)

    digest = hmac.new(secret_key.encode('utf8'), payload.encode('utf8'), digestmod=sha256).digest()
    signature = base64.b64encode(digest).decode()

    suffix = '{}&Signature={}'.format(suffix, parse.quote(signature))
    return suffix

def post(access_key:str, secret_key:str, host:str, path:str, data:dict = None)->json:
    try:
        url = 'http://{}{}?{}'.format(host, path, __get_post_url_suffix(access_key, secret_key, host, path))
        headers = {'Accept':'application/json', 'Content-type':'application/json'}
        res = requests.post(url, json=data, headers = headers)
        data = res.json()
        return data
    except Exception as e:
        logger.error(e)
    return None