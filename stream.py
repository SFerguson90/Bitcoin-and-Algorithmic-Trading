# IMPORTS
import os
from dotenv import load_dotenv
import websocket, json

# ALPACA SOCKET CONNECTION
socket = "wss://data.alpaca.markets/stream"

# LOAD THE .ENV FILE
load_dotenv(verbose=True)

# SET ALPACA API KEYS FROM .ENV FILE
alpaca_api_key = os.getenv("ALPACA_API_KEY")
alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

###### FUNCTIONS / DICTIONARIES TO SEND / MESSAGES

# OPEN
def on_open(ws):
    print("Opening Connectionn to Alpaca API Services")
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
            "streams":["T.SPY"]
        }
    }

    ws.send(json.dumps(channel_data))

def on_message(ws, message):
    print("\n", "="*30, "MESSAGE", "="*30, "\n\n",message,'\n')

# CLOSE
def on_close(ws):
    print("Closing Connection to Alpaca API Services")

# SOCKET OBJECT INSTANTIATED 
ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)

# GO GO GO
ws.run_forever()

## LISTEN ALL
#{"action": "listen", "data": {"streams": ["T.SPY"]}}

## MINUTE BARS
#{"action": "listen", "data": {"streams": ["AM.SPY"]}}