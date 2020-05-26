

## An Asynchronous Event-driven High-frequency Trading System for MarketMakers、Liquidity providers and other HFT users.
## Architecture

![Architecture](https://raw.githubusercontent.com/hbdmapi/hbdm_Python/master/docs/framework.png)

   ### 1、Market Module
    Realtime Orderbook、kline、market trade details are subscribed by websocket for strategies callback.Huobi Swap and Huobi Future has been integrated.
   ### 2、RestFul API Module
    APIs of Huobi Swap and Huobi Future has been integrated such as trade api、batch trade api、cancel api,etc. 
   ### 3、Asset Module
    Assets are subscribed by websocket for strategies callback.Huobi Swap and Huobi Future has been integrated.
   ### 4、Position Module
    Positions are subscribed by websocket for strategies callback.Huobi Swap and Huobi Future has been integrated.
   ### 5、Order Module
    Orders are subscribed by websocket for strategies callback.Huobi Swap and Huobi Future has been integrated.
   ### 6、Logging Module
    Logs can log to files corresponding to different levels such as "DEBUG","INFO","WARN", "ERROR".
   ### 7、Trading Module
    Common trade interface and cancel interface,etc.
   ### 8、ErrorHandle Module
    websocket automatic reconnection mechanism, heartbeat mechanism,etc. 
   ### 9、RiskControl Module
    DingDing message Alarm,etc.
   ### 10、It Can do More
    ...
    
## Install Steps
    python:python 3.5.3 above
    git clone https://github.com/hbdmapi/hbdm_Python.git
    pip install . --ignore-installed

## Quick Start
   - cd examples
   - cd huobi_swap
   - edit "config.json"
     - "access_key": "api access_key"
     - "secret_key": "api secret_key"
     - you may also have to change the host and wss address.
        
     - save and quit.
   - bash run.sh
   - Happy Trading

## Demo Tutorial
Demo strategy only implements a simple sell short and close short strategy.

> NOTE: The demo strategy needs to be modified to run in production。


## Strategy dirs:
```text
ProjectName
    |----- docs
    |       |----- README.md
    |----- scripts
    |       |----- run.sh
    |----- config.json
    |----- main.py
    |----- strategy
    |      |----- strategy1.py
    |      |----- strategy2.py
    |      |----- ...
    |----- .gitignore
    |----- README.md
```

#### Strategy Config

Strategy config file [config.json](config.json):

- ACCOUNTS `list` your hdbm account name；
- strategy `string` your strategy name;
- symbol `string` the trade code,such as BTC-USD
- MARKETS `list` the market config.

> Config Tutorials: [config tutorials](/docs/config/README.md)


#### Run

```text
python main.py config.json
```

## Suggestions and Bugs

Pls post your suggestions and bugs in [issues](https://github.com/hbdmapi/hbdm_Python/issues)

## Reference
TheNextQuant

