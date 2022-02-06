#!/usr/bin/env python3

import websocket
import _thread
import time

def on_message(ws, message):
    if 'players' not in message:
        print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

if __name__ == "__main__":
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:3000",
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()
