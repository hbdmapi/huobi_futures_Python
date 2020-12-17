# -*- coding:utf-8 -*-

from distutils.core import setup


setup(
    name="alphaquant",
    version="1.1.5",
    packages=[
        "alpha",
        "alpha.utils",
        "alpha.platforms",
    ],
    description="Asynchronous driven quantitative trading framework.",
    url="https://github.com/hbdmapi/hbdm_python",
    author="qiaoxiaofeng",
    author_email="andyjoe318@gmail.com",
    license="MIT",
    keywords=[
        "alphaquant", "huobi future", "async", "asynchronous", "btc",
        "marketmaker", "huobi", "huobi swap", "strategy"
    ],
    install_requires=[
        "aiohttp==3.6.2",
        "motor==2.0.0"
    ],
)