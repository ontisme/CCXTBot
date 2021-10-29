from linebot.models import FlexSendMessage


def init_platform_api(action_time):
    flex_message = FlexSendMessage(
        alt_text="初始化設定",
        contents={
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "請選擇您使用的交易所",
                                "color": "#ffffff",
                                "size": "xl",
                                "flex": 4,
                                "weight": "bold"
                            }
                        ]
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "Binance 幣安",
                            "data": "{\"time\": \"" + action_time + "\", \"message\": {\"page\": \"init_platform_api\", \"platform\": \"binance\", \"action\": \"init_platform_api\"}}",
                            "displayText": "使用 幣安"
                        },
                        "style": "primary",
                        "height": "md",
                        "offsetTop": "xxl",
                        "color": "#FCA535"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "FTX",
                            "data": "{\"time\": \"" + action_time + "\", \"message\": {\"page\": \"init_platform_api\", \"platform\": \"ftx\", \"action\": \"init_platform_api\"}}",
                            "displayText": "使用 FTX"
                        },
                        "style": "primary",
                        "height": "md",
                        "offsetTop": "xxl",
                        "color": "#00B4C9"
                    }
                ],
                "paddingAll": "20px",
                "backgroundColor": "#222222",
                "spacing": "md",
                "height": "225px",
                "paddingTop": "22px"
            }
        }
    )
    return flex_message


def menu(action_time):
    flex_message = FlexSendMessage(
        alt_text="操作清單",
        contents={
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "請選擇您使用的交易所",
                                "color": "#ffffff",
                                "size": "xl",
                                "flex": 4,
                                "weight": "bold"
                            }
                        ]
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "Binance 幣安",
                            "data": "{\"time\": \"" + action_time + "\", \"message\": {\"page\": \"init_platform_api\", \"platform\": \"binance\", \"action\": \"init_platform_api\"}}",
                            "displayText": "使用 幣安"
                        },
                        "style": "primary",
                        "height": "md",
                        "offsetTop": "xxl",
                        "color": "#FCA535"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "FTX",
                            "data": "{\"time\": \"" + action_time + "\", \"message\": {\"page\": \"init_platform_api\", \"platform\": \"ftx\", \"action\": \"init_platform_api\"}}",
                            "displayText": "使用 FTX"
                        },
                        "style": "primary",
                        "height": "md",
                        "offsetTop": "xxl",
                        "color": "#00B4C9"
                    }
                ],
                "paddingAll": "20px",
                "backgroundColor": "#222222",
                "spacing": "md",
                "height": "225px",
                "paddingTop": "22px"
            }
        }
    )
    return flex_message


def trade_info_confirm(action_time, market, min_price, max_price, batch_count, totalOrderAmount, usdtBalance):
    flex_message = FlexSendMessage(
        alt_text="交易資訊",
        contents={
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "交易對",
                                "color": "#ffffff66",
                                "size": "sm"
                            },
                            {
                                "type": "text",
                                "text": market,
                                "color": "#ffffff",
                                "size": "xl",
                                "flex": 4,
                                "weight": "bold"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "區間價格",
                                        "color": "#ffffff66",
                                        "size": "sm"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"{min_price} - {max_price}",
                                        "color": "#ffffff",
                                        "size": "xl",
                                        "flex": 4,
                                        "weight": "bold"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "網格數量",
                                        "color": "#ffffff66",
                                        "size": "sm"
                                    },
                                    {
                                        "type": "text",
                                        "text": batch_count,
                                        "color": "#ffffff",
                                        "size": "xl",
                                        "flex": 2,
                                        "weight": "bold"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "可用餘額",
                                        "color": "#ffffff",
                                        "size": "sm",
                                        "align": "start",
                                        "weight": "bold",
                                        "flex": 2
                                    },
                                    {
                                        "type": "text",
                                        "text": f"{usdtBalance} USDT",
                                        "color": "#ffffff",
                                        "size": "sm",
                                        "flex": 4,
                                        "weight": "bold",
                                        "align": "end"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "成交額",
                                        "color": "#ffffff",
                                        "size": "xl",
                                        "align": "start",
                                        "weight": "bold",
                                        "flex": 2
                                    },
                                    {
                                        "type": "text",
                                        "text": f"{totalOrderAmount} USDT",
                                        "color": "#ffffff",
                                        "size": "xl",
                                        "flex": 4,
                                        "weight": "bold",
                                        "align": "end"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "postback",
                                    "label": f"買入 {market}\n總成交額：*{totalOrderAmount}*",
                                    "data": "{\"time\": \"" + action_time + "\", \"message\": {\"page\": \"trade_info_confirm\", \"action\": \"trade\", \"param\": {\"market\": \"\", \"side\": \"buy\", \"min_price\": " + min_price + ", \"max_price\": " + max_price + ", \"batch_count\": " + batch_count + ", \"total_price\": " + totalOrderAmount + "}}}"
                                },
                                "style": "primary",
                                "height": "md",
                                "offsetTop": "none",
                                "color": "#22AA22"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "postback",
                                    "label": f"賣出 {market}\n總成交額：*{totalOrderAmount}*",
                                    "data": "{\"time\": \"" + action_time + "\", \"message\": {\"page\": \"trade_info_confirm\", \"action\": \"trade\", \"param\": {\"market\": \"\", \"side\": \"sell\", \"min_price\": " + min_price + ", \"max_price\": " + max_price + ", \"batch_count\": " + batch_count + ", \"total_price\": " + totalOrderAmount + "}}}"
                                },
                                "style": "primary",
                                "height": "md",
                                "offsetTop": "none",
                                "color": "#DD2222"
                            }
                        ],
                        "spacing": "lg",
                        "margin": "xxl"
                    }
                ],
                "paddingAll": "20px",
                "backgroundColor": "#222222",
                "spacing": "md",
                "height": "325px",
                "paddingTop": "22px"
            }
        }
    )
    return flex_message


def my_wallet(wallet):
    print(wallet)
    coin_list = [
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "您的錢包",
                    "color": "#ffffff",
                    "size": "xl",
                    "flex": 4,
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "color": "#ffffff",
                    "size": "md",
                    "flex": 4,
                    "weight": "bold",
                    "text": f"資產估值 ≈ " + str(round(wallet["totalValue"], 2)) + " USDT"
                }
            ]
        },
        {
            "type": "separator"
        },
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": "幣種",
                    "size": "sm",
                    "color": "#FFFFFF"
                },
                {
                    "type": "text",
                    "text": "數量",
                    "size": "sm",
                    "color": "#FFFFFF"
                },
                {
                    "type": "text",
                    "text": "價值",
                    "size": "sm",
                    "color": "#FFFFFF"
                }
            ]
        },
    ]

    for i in wallet["wallet"]:
        content = {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": i["coin"],
                    "size": "sm",
                    "color": "#FFFFFF"
                },
                {
                    "type": "text",
                    "text": str(round(float(i["total"]), 7)),
                    "size": "sm",
                    "color": "#FFFFFF"
                },
                {
                    "type": "text",
                    "text": "US$" + str(round(float(i["usdValue"]), 2)),
                    "size": "sm",
                    "color": "#FFFFFF"
                }
            ]
        }
        coin_list.append(content)
    print(coin_list)
    flex_message = FlexSendMessage(
        alt_text="我的錢包",
        contents={
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": coin_list,
                "paddingAll": "20px",
                "backgroundColor": "#222222",
                "spacing": "md",
                "height": "225px",
                "paddingTop": "22px"
            }
        }
    )

    print(flex_message)
    return flex_message
