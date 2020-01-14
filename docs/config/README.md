
## 配置文件

框架启动的时候，需要指定一个 `json` 格式的配置文件。

## 配置使用
所有 `config.json` 配置文件里的 `key-value` 格式数据，都可以通过如下方式使用：
```python
from alpha.config import config

config.name  # 使用配置里的name字段
config.abc  # 使用配置里的abc字段
```

## 系统配置参数
> 所有系统配置参数均为 `大写字母` 为key;  
> 所有系统配置参数均为 `可选`;  


##### 1. LOG
日志配置。包含如下配置：

**示例**:
```json
{
    "LOG": {
        "console": false,
        "level": "DEBUG",
        "path": "/var/log/servers/Quant",
        "name": "quant.log",
        "clear": true,
        "backup_count": 5
    }
}
```

**配置说明**:
- console `boolean` 是否打印到控制台，`true 打印到控制台` / `false 打印到文件`，可选，默认为 `true`
- level `string` 日志打印级别 `DEBUG`/ `INFO`，可选，默认为 `DEBUG`
- path `string` 日志存储路径，可选，默认为 `/var/log/servers/Quant`
- name `string` 日志文件名，可选，默认为 `quant.log`
- clear `boolean` 初始化的时候，是否清理之前的日志文件，`true 清理` / `false 不清理`，可选，默认为 `false`
- backup_count `int` 保存按天分割的日志文件个数，默认0为永久保存所有日志文件，可选，默认为 `0`


##### 2. HEARTBEAT
服务心跳配置。

**示例**:
```json
{
    "HEARTBEAT": {
        "interval": 3,
        "broadcast": 0
    }
}
```

**配置说明**:
- interval `int` 心跳打印时间间隔(秒)，0为不打印 `可选，默认为0`
- broadcast `int` 心跳广播时间间隔(秒)，0为不广播 `可选，默认为0`


##### 3. PROXY
HTTP代理配置。
大部分交易所在国内访问都需要翻墙，所以在国内环境需要配置HTTP代理。

**示例**:
```json
{
    "PROXY": "http://127.0.0.1:1087"
}
```

**配置说明**:
- PROXY `string` http代理，解决翻墙问题

> 注意: 此配置为全局配置，将作用到任何HTTP请求，包括Websocket；

##### 4. MARKET
MARKET行情配置。

示例：
```json
"MARKETS": [
        {
            "platform": "huobi_swap",
            "symbols": ["BTC-USD"],
            "channels":[
                "orderbook", "kline", "trade"
            ],
            "orderbook_length": 10,
            "orderbooks_length": 100,
            "klines_length": 100,
            "trades_length": 100,
            "wss": "wss://api.btcgateway.pro"

        }
    ]
```
配置说明：
- platform: `string` 平台名
- channels: `list` 订阅的频道比如orderbook, kline, trade
- symbols: `list` 订阅的交易对
- orderbook_length: `int` 推送的orderbook的最大长度
- orderbooks_length: `int` orderbook队列的最大长度
- klines_length: `int` klines队列的最大长度
- trades_length: `int` trades队列的最大长度
- wss: `string` wss行情订阅地址

##### 5. 其他说明：

- SERVER_ID `string`  策略实例标示
- strategy `string`  策略名字