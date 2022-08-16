import websocket


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.create_connection("ws://linode.liquidco.in:8000/?uid=111")
    # ws.recv()
    print("Sending echo...")
    ws.send('{"cmd":"echo","msg":"hi3"}')
    print("Sent")
    print("Receiving...")
    result = ws.recv()
    print("Received '%s'" % result)
    ws.close()