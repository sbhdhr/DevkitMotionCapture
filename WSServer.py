from simple_websocket_server import WebSocketServer, WebSocket
import Globals


class WSServer(WebSocket):

    def handle(self):
        print(f"WSServer:: Received Data:{self.data}")

        cltData = [float(s) for s in self.data.split(';')]

        if Globals.ws_verbose:
            print(f"WSServer:: Parsed data:\nx:{cltData[0]}\ny:{cltData[1]}\nz:{cltData[2]}\n\n")


        # throttle incoming data
        Globals.xdot = Globals.ydot
        Globals.ydot = tuple(cltData)
        Globals.viz_update_flag = True

        self.send_message(f"Ack")
