from fastapi import FastAPI
import user as user_module
import order as order_module
from dotenv import load_dotenv
import os
import json
from pydantic import BaseModel
from AI.trend_calculation import trend_prediction


class Order(BaseModel):
    pair: str
    type: str | None = None
    volume: str

load_dotenv()

# Get PUBLIC_KEY and PRIVATE_KEY from .env
PUBLIC_KEY = os.getenv('PUBLIC_KEY')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')

#Get WebSocketToken
# WEBSOCKETTOKEN = GetWebSocketToken.get_token(PUBLIC_KEY, PRIVATE_KEY)

app = FastAPI()

qty = 0.0
trade_value = 0.0
trend ="Long"
trend_status = "Normal"
# trend, trend_status = trend_prediction()

# Get User Balance
@app.get("/user/balance")
async def get_balance():
    # print(user.get_balance())
    # print (type(user.get_balance))
    response = user_module.get_balance()
    error = response['error']
    result = response['result']
    balance = 0.0
    if error is not None:
        try:
            balance = result['USDT']
        except:
            balance = 0.0
        return balance
    else:
        return error

# Create Order
@app.post("/order/create/")
async def create_order(order: Order):
    trend, trend_status = trend_prediction()
    global qty, trade_value
    if order.type == 'buy' and trend == "Long" or order.type == 'sell' and trend == "Short":
        response = user_module.get_balance()
        error = response['error']
        result = response['result']
        try:
            balance = result['USDT']
            balance = float(balance)
            print(balance)
        except:
            balance = 0.0
        if balance == 0.0:
            return "Not enough"
        else:
            # qty = balance / 4
            qty = 0.1
            trade_value = 100
            response = order_module.create_order(order.pair, order.type, qty)
            print(response)
    elif order.type == "exit_buy" or trend_status == "Bearish divergence detected":
        if qty == 0:
            return "No postion"
        volume = qty * (0.0 - float(order.volume)) / 100
        trade_value = trade_value + float(order.volume)
        response = order_module.create_order(order.pair, "sell", volume)
    elif order.type == "exit_sell" or trend_status == "Bullish divergence detected":
        if qty == 0:
            return "No postion"
        volume = qty * float(order.volume) / 100
        trade_value = trade_value - float(order.volume)
        response = order_module.create_order(order.pair, "buy", volume)
    # print(response)
    return response
