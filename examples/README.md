### examples 使用说明

# 简介
    examples文件夹里面分别有对应火币交割合约、火币永续合约、火币期权合约(内测中)的例子，例子中的config.json代表合约的各种典型设置(比如symbol的配置使用等)，strategy.py文件则是对应合约从订阅行情、订阅订单推送、仓位推送、账户推送到restful下撤单等的典型使用。

    通过例子的使用，您可以初步学会如何使用该框架去编写您自己的策略。

# 运行
    配置好config.json文件后，
    bash run.sh
    就可以看到行情、订单、账户等信息等推送以及下撤单等功能的演示；

# 帮助
    有使用问题请在https://github.com/hbdmapi/hbdm_Python/issues 发帖提问；
    