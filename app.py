# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

import json
import re
import sqlite3
import threading
from time import sleep, time
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, PostbackEvent
import client
import database
import linebot_template
from datetime import datetime
import os

# 基本設定
line_bot_api = LineBotApi(
    "Pu9RNSO/N5lUmDDQf7wMTMpTHcvLe90lDXhOt5Y1Xqf0hE4Le1wwILKcajO/RJ8+T+acOS6v+kVY/G2K/0q9mjdJdssOHmubifFoNuxEerGDJbGVPT5tyMTXNw6NgfkS5EkSZoG85Ez2muBZFO0lKAdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("fb7994472d6108810b93dfd71af28b64")
app = Flask(__name__, static_url_path='', )
db = database
template = linebot_template


@app.route("/")
def hello():
    return "Flask on port 5000"

if __name__ == "__main__":
    # a = {
    #     "time": "2021-10-28 10:43:34",
    #     "message": {
    #         "page": "trade_info_confirm",
    #         "action": "trade",
    #         "param": {
    #             "market": "",
    #             "side": "",
    #             "min_price": 0,
    #             "max_price": 0,
    #             "batch_count": 0,
    #             "total_price": 0
    #         }
    #     }
    # }
    #
    # print(a)
    port = int(os.environ.get('PORT', 33456))
    app.run(host="0.0.0.0", port=port)
