# -*- coding:utf-8 -*-

"""
DingTalk Bot API.
https://open-doc.dingtalk.com/microapp/serverapi2/qf2nxq

"""

from alpha.utils.request import AsyncHttpRequests


class DingTalk:
    """ DingTalk Bot API.
    """
    BASE_URL = "https://oapi.dingtalk.com/robot/send?access_token="

    @classmethod
    async def send_text_msg(cls, access_token, content, phones=None, is_at_all=False):
        """ Send text message.

        Args:
            access_token: DingTalk Access Token.
            content: Message content to be sent.
            phones: Phone numbers to be @.
            is_at_all: Is @ all members? default is False.
        """
        body = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        if is_at_all:
            body["at"] = {"isAtAll": True}
        if phones:
            assert isinstance(phones, list)
            body["at"] = {"atMobiles": phones}
        url = cls.BASE_URL + access_token
        headers = {"Content-Type": "application/json"}
        await AsyncHttpRequests.post(url, data=body, headers=headers)

    @classmethod
    async def send_markdown_msg(cls, access_token, title, text, phones=None, is_at_all=False):
        """ Send markdown message.

        Args:
            access_token: DingTalk Access Token.
            title: Message title.
            text: Message content to be sent.
            phones: Phone numbers to be @.
            is_at_all: Is @ all members? default is False.
        """
        body = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            }
        }
        if is_at_all:
            body["at"] = {"isAtAll": True}
        if phones:
            assert isinstance(phones, list)
            body["at"] = {"atMobiles": phones}
        url = cls.BASE_URL + access_token
        headers = {"Content-Type": "application/json"}
        await AsyncHttpRequests.post(url, data=body, headers=headers)
