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


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        # print (body, signature)
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = str(event.message.text).strip()  # 使用者輸入的內容
    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name  # 使用者名稱
    uid = profile.user_id  # 發訊者ID
    current_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(f"[{current_time}] 接收到：{user_name}({uid}) => {msg}")
    # ================================
    user = db.get_userInfo(uid)
    # 如果已開通
    if user:
        if msg == "!刪除帳號":
            ret = db.del_userInfo(uid)
            if ret:
                content = TextSendMessage(text=f'您的API資料已經刪除完畢')
                line_bot_api.reply_message(event.reply_token, content)
            else:
                content = TextSendMessage(text=f'刪除失敗，請找作者手動刪除')
                line_bot_api.reply_message(event.reply_token, content)
        elif msg == "!清空委託":
            c = client.TradeClient(user["platform"], user["api_key"], user["api_secret"])
            ret = c.cancel_all_orders()
            if ret:
                content = TextSendMessage(text='清空完畢！')
                line_bot_api.reply_message(event.reply_token, content)
            else:
                content = TextSendMessage(text='清空失敗！')
                line_bot_api.reply_message(event.reply_token, content)

        # 如果還沒有填入APIKEY
        elif user["api_key"] == "" or user["api_secret"] == "":
            if "APIKEY=" in msg:
                _apikey = msg.split('=')[1]
                db.edit_userInfo(uid, api_key=_apikey)
                if user["platform"] == "binance":
                    contents = TextSendMessage(
                        text=f'請依照格式輸入【Binance 幣安】交易所提供的 API SECRET\n\nAPISECRET=這邊替換成你的API SECRET')
                    line_bot_api.reply_message(event.reply_token, contents)

                elif user["platform"] == "ftx":
                    contents = TextSendMessage(text=f'請依照格式輸入【FTX】交易所提供的 API SECRET\n\nAPISECRET=這邊替換成你的API SECRET')
                    line_bot_api.reply_message(event.reply_token, contents)
                pass
            elif "APISECRET=" in msg:
                _apisecret = msg.split('=')[1]
                db.edit_userInfo(uid, api_key=user["api_key"], api_secret=_apisecret)
                user = db.get_userInfo(uid)
                if user["platform"] != "" and user["api_key"] != "" and user["api_secret"] != "":
                    contents = TextSendMessage(text=f'設定完畢，可以開始交易了')
                    line_bot_api.reply_message(event.reply_token, contents)
        elif "!" in msg:
            c = client.TradeClient(user["platform"], user["api_key"], user["api_secret"])
            k = re.findall("!(.+?),(\d+),(\d+),(\d+),(\d+)", msg)
            if k:
                k = k[0]
                market = f"{k[0]}/USDT".upper()
                min_price = k[1]
                max_price = k[2]
                batch_count = k[3]
                total_order_amount = f"{k[4]}"
                usdt_balance = 0

                for i in c.get_wallet()["wallet"]:
                    if i["coin"] == "USDT":
                        usdt_balance = i["free"]

                if usdt_balance < total_order_amount:
                    contents = TextSendMessage(text=f'USDT 餘額不足')
                    line_bot_api.reply_message(event.reply_token, contents)
                else:
                    content = linebot_template.trade_info_confirm(current_time,market, min_price, max_price, batch_count,
                                                                  total_order_amount, usdt_balance)
                    line_bot_api.reply_message(event.reply_token, content)
        else:
            c = client.TradeClient(user["platform"], user["api_key"], user["api_secret"])
            wallet = c.get_wallet()
            content = linebot_template.my_wallet(wallet)
            line_bot_api.reply_message(event.reply_token, content)

    else:
        # 如果沒使用過，提示初始化設定
        contents = [
            TextSendMessage(text=f'第一次使用須設定交易平台與API參數'),
            template.init_platform_api(current_time)
        ]
        line_bot_api.reply_message(event.reply_token, contents)


@handler.add(PostbackEvent)
def handle_postback(event):
    msg = json.loads(str(event))
    uid = msg['source']['userId']
    current_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # 回傳資訊
    data = json.loads(msg['postback']['data'])

    #
    # 回傳格式
    # {'time': '2021-10-28 10:43:34', 'message': {'page': 'init_platform_api', 'platform': 'ftx', 'action': 'init_platform_api'}}
    #

    # 操作超過一分鐘，拒絕訪問
    try:
        diff_time = datetime.now().timestamp() - datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S").timestamp()
        if diff_time > 60:
            line_bot_api.push_message(uid, TextSendMessage(text=f'操作限在1分鐘內完成操作，如逾時請重新操作！'))
            return
    except:
        pass

    if data["message"]["page"] == "init_platform_api":
        if data["message"]["platform"] == "binance":
            db.add_userInfo(uid, data["message"]["platform"], "", "", current_time)
            contents = TextSendMessage(text=f'請依照格式輸入【Binance 幣安】交易所提供的 API KEY\n\nAPIKEY=這邊替換成你的API KEY')
            line_bot_api.reply_message(event.reply_token, contents)
        elif data["message"]["platform"] == "ftx":
            db.add_userInfo(uid, data["message"]["platform"], "", "", current_time)
            contents = TextSendMessage(text=f'請依照格式輸入【FTX】交易所提供的 API KEY\n\nAPIKEY=這邊替換成你的API KEY')
            line_bot_api.reply_message(event.reply_token, contents)
    elif data["message"]["page"] == "trade_info_confirm":
        # {'time': '2021-10-28 10:43:34', 'message': {'page': 'trade_info_confirm', 'action': 'trade', 'param': {'market': '', 'side': '', 'min_price': 0, 'max_price': 0, 'batch_count': 0, 'total_price': 0}}}
        if data["message"]["page"]["action"] == "trade":
            user = db.get_userInfo(uid)
            c = client.TradeClient(user["platform"], user["api_key"], user["api_secret"])
            info = json.loads(data["message"]["page"]["param"])
            ret = c.create_order_in_range(info["market"], info["side"], info["min_price"], info["max_price"],
                                    info["batch_count"], info["total_price"])
            if ret:
                wallet = c.get_wallet()
                contents = [
                    TextSendMessage(text=f'委託成功'),
                    linebot_template.my_wallet(wallet)
                ]
                line_bot_api.reply_message(event.reply_token, contents)

# 傳圖片
def send_image(uid, image_url):
    image = ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
    line_bot_api.push_message(uid, image)

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
