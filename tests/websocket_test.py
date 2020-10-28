#!/usr/bin/env python

import datetime
import uuid
import urllib
import asyncio
import websockets
import json
import hmac
import base64
import hashlib
import gzip
import traceback

        

def generate_signature(host, method, params, request_path, secret_key):
    """Generate signature of huobi future.
    
    Args:
        host: api domain url.PS: colo user should set this host as 'api.hbdm.com',not colo domain.
        method: request method.
        params: request params.
        request_path: "/notification"
        secret_key: api secret_key

    Returns:
        singature string.

    """
    host_url = urllib.parse.urlparse(host).hostname.lower()
    sorted_params = sorted(params.items(), key=lambda d: d[0], reverse=False)
    encode_params = urllib.parse.urlencode(sorted_params)
    payload = [method, host_url, request_path, encode_params]
    payload = "\n".join(payload)
    payload = payload.encode(encoding="UTF8")
    secret_key = secret_key.encode(encoding="utf8")
    digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    return signature

async def subscribe(url, access_key, secret_key, subs, callback=None, auth=False):
    """ Huobi Future subscribe websockets.

    Args:
        url: the url to be signatured.
        access_key: API access_key.
        secret_key: API secret_key.
        subs: the data list to subscribe.
        callback: the callback function to handle the ws data received. 
        auth: True: Need to be signatured. False: No need to be signatured.

    """
    async with websockets.connect(url) as websocket:
        if auth:
            timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
            data = {
                "AccessKeyId": access_key,
                "SignatureMethod": "HmacSHA256",
                "SignatureVersion": "2",
                "Timestamp": timestamp
            }
            sign = generate_signature(url,"GET", data, "/linear-swap-notification", secret_key)
            data["op"] = "auth"
            data["type"] = "api"
            data["Signature"] = sign
            msg_str = json.dumps(data)
            await websocket.send(msg_str)
            print(f"send: {msg_str}")
        for sub in subs:
            sub_str = json.dumps(sub)
            await websocket.send(sub_str)
            print(f"send: {sub_str}")
        while True:
            rsp = await websocket.recv()
            data = json.loads(gzip.decompress(rsp).decode())
            print(f"recevie<--: {data}")
            if "op" in data and data.get("op") == "ping":
                pong_msg = {"op": "pong", "ts": data.get("ts")}
                await websocket.send(json.dumps(pong_msg))
                print(f"send: {pong_msg}")
                continue
            if "ping" in data: 
                pong_msg = {"pong": data.get("ping")}
                await websocket.send(json.dumps(pong_msg))
                print(f"send: {pong_msg}")
                continue
            rsp = await callback(data)

async def handle_ws_data(*args, **kwargs):
    """ callback function
    Args:
        args: values
        kwargs: key-values.
    """
    print("callback param", *args,**kwargs)

if __name__ == "__main__":
    ####  input your access_key and secret_key below:
    access_key = ""
    secret_key = ""

    market_url = 'ws://api.hbdm.vn/linear-swap-ws'
    order_url = 'wss://api.hbdm.vn/linear-swap-notification'
    
    market_subs = [
                   
                {
                    "sub": "market.BTC-USDT.kline.1min.open",
                    "id": "id1"
                },
                {
                    "sub": "market.BTC-USDT.depth.step0",
                    "id": "id1"
                }

            ]
    order_subs = [
                {
                    "op": "sub",
                    "cid": str(uuid.uuid1()),
                    "topic": "orders.BTC-USDT"
                },
                {
                    "op": "sub",
                    "cid": str(uuid.uuid1()),
                    "topic": "positions.BTC-USDT"
                },
                {
                    "op": "sub",
                    "cid": str(uuid.uuid1()),
                    "topic": "accounts.BTC-USDT"
                }

            ]

    while True: 
        try:
            asyncio.get_event_loop().run_until_complete(subscribe(market_url, access_key,  secret_key, market_subs, handle_ws_data, auth=False))
            #asyncio.get_event_loop().run_until_complete(subscribe(order_url, access_key,  secret_key, order_subs, handle_ws_data, auth=True))
        #except (websockets.exceptions.ConnectionClosed):
        except Exception as e:
            traceback.print_exc()
            print('websocket connection error. reconnect rightnow')
