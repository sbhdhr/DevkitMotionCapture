from simple_websocket_server import WebSocketServer, WebSocket
import Globals

class WSServer(WebSocket):

    def handle(self):
        print(f"WSServer:: Received Data:{self.data}")

        with open(Globals.filename, 'a+') as file:
            file.write(self.data)
            file.write('\n')

        cltData = [float(s) for s in self.data.split(';')]

        # alter the data here

        # Scale X axis
        cltData[0] = cltData[0] / 1000
        # Scale Y axis
        cltData[1]=cltData[1]/1000

        # Scale Z axis
        cltData[2]=cltData[2]/1000

        if Globals.ws_verbose:
            print(f"WSServer:: Parsed data:\nx:{cltData[0]}\ny:{cltData[1]}\nz:{cltData[2]}\n\n")


        # throttle incoming data
        Globals.xdot = Globals.ydot
        Globals.ydot = (cltData[0],cltData[1],cltData[2])
        Globals.viz_update_flag = True

        #self.send_message(f"Ack")
