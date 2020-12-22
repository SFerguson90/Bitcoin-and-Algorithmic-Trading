# IMPORTS
import os, websocket, json, pprint
import plotly.graph_objects as go
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime


# VARIABLES
symbol = "TSLA"
times = list()
prices = list()

# ALPACA SOCKET CONNECTION
socket = "wss://data.alpaca.markets/stream"

# LOAD THE .ENV FILE
load_dotenv(verbose=True)

# SET ALPACA API KEYS FROM .ENV FILE
alpaca_api_key = os.getenv("ALPACA_API_KEY")
alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

# INSTANTIATE FIGURE WIDGET
fig = go.FigureWidget()
fig.layout.title = f"{symbol}"
fig.show()

# INSTANTIATE DATAFRAME
df = pd.DataFrame()

###### FUNCTIONS / DICTIONARIES TO SEND / MESSAGES

# OPEN
def on_open(ws):
    print("Opening Connection to Alpaca API Services")
    auth_data = {
        "action": "authenticate",
        "data": {
            "key_id": alpaca_api_key,
            "secret_key": alpaca_secret_key
            }
        }

    ws.send(json.dumps(auth_data))

    channel_data = {
        "action": "listen",
        "data": {
            "streams":[f"Q.{symbol}"]
        }
    }

    ws.send(json.dumps(channel_data))

def on_message(ws, message):
    #print("\n", "="*30, "MESSAGE", "="*30, "\n\n",message,'\n')

    # Turn string into dictionary
    message_data = json.loads(message)

    global times
    global prices

    # VARIABLES
    if message_data["data"]["ev"] == 'Q':
        
        # VARIABLES FOR QUOTE SCHEMA
        data_symbol = message_data["data"]["T"]
        nano_time = message_data["data"]["t"]
        bid_size = message_data["data"]["s"]
        bid_price = message_data["data"]["p"]
        ask_size = message_data["data"]["S"]
        ask_price = message_data["data"]["P"]

        time = datetime.now()
        times.append(time)
        prices.append(float(ask_price))
        with fig.batch_update():
            fig.data[0].x = times
            fig.data[0].y = prices

    if message_data["data"]["ev"] == 'T':

        # VARIABLES FOR TRADE SCHEMA
        data_symbol = message_data["data"]["T"]
        nano_time = message_data["data"]["t"]
        trade_size = message_data["data"]["s"]
        trade_price = message_data["data"]["p"]

    if message_data["data"]["ev"] == 'AM':

        # VARIABLES FOR MINUTE BAR SCHEMA
        data_symbol = message_data["data"]["T"]
        open_price = message_data["data"]["o"]
        high_price = message_data["data"]["h"]
        low_price = message_data["data"]["l"]
        close_price = message_data["data"]["c"]

# CLOSE
def on_close(ws):
    print("Closing Connection to Alpaca API Services")

# SOCKET OBJECT INSTANTIATED 
ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)

# GO GO GO
ws.run_forever()