from Visualizer import Visualizer
from WSServer import WSServer
from simple_websocket_server import WebSocketServer, WebSocket
from threading import Thread


def runServer():
    print("Main:: Started backend WS server. Listening at port: 8765")
    server = WebSocketServer('localhost', 8765, WSServer)
    server.serve_forever()


if __name__ == '__main__':

    ws_run = Thread(target=runServer)
    ws_run.start()

    v = Visualizer(refresh_int=10)
    v.animation()

'''


'''
