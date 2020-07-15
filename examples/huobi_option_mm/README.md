## 策略说明

本策略为期权简易做市策略，使用标记价格mark_price加上一定的价差来挂买单与卖单，每次会根据标记价格来撤销委托的卖单与买单，持有的期权持仓风险delta,超过一定值则通过火币永续合约进行对冲使得delta保持0。

## delta计算

i. 假设期权BTC总delta为 `Do`,期权的持仓(BTC)账户权益(margin_balance)为`Mo`,获取到的期权的持仓(BTC)delta为 `Dp`，则:

            Do = Dp + Mo

ii. 假设火币永续合约BTC总delta为`Ds`,的账户权益(BTC)（margin_balance）为`Ms`,持有的多仓(BTC)张数为`Ls`,持有的空仓(BTC)张数为`Ss`，当前BTC最新价为`Ps`,则:

            Ds = Ms + Ls*100/Ps - Ss*100/Ps

iii. 假设总delta为`D`，则:

            D = Do + Ds

iv. 如果abs(D)>=阈值：

    如果D>=0,则在永续卖空 int(D*Ps/100) 张的仓位；

    如果D<0,则在永续买多 int((abs(D)*Ps/100)) 张的仓位；


## 策略使用说明

策略启动的时候，需要指定一个 `json` 格式的配置文件。请参考配置文件config.json的说明：[配置文件](/docs/config/README.md)

可以参照例子的config.json进行对应配置，其中

`orderbook_invalid_seconds`：orderbook无效时间，收到的orderbook时间戳超过多少S认为是无效的；

`spread`: 摆盘价差

`quantity`: 每次摆盘数量

`max_quantity`: 多仓的最大仓位数量和空仓的最大数量

`delta_limit`: delta对冲阈值

`swap_volume_usd`: 永续合约张数USD价值

## 策略运行

```shell
bash run.sh
```
