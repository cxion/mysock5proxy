import socket, select, SocketServer, struct
from threading import current_thread

class ProxyServer(SocketServer.StreamRequestHandler):
    def handle(self):

            clientProxy = self.connection
            data = clientProxy.recv(3) #05 10 00    -->  want serve
            clientProxy.send("\x05\x00")#05 00     <---  can serve
            data = clientProxy.recv(4)  #05 01 00 01/03   --->ver cmd 00 addr port
            for x in data:
                print hex(ord(x)),
            print ''
            protocol = ord(data[1])
            Tpye = ord(data[3])
            if Tpye == 1:
                addr = clientProxy.recv(4)
            elif Tpye == 3:
                n = ord(clientProxy.recv(1))
                addr = clientProxy.recv(n)
            port = struct.unpack('>H', self.rfile.read(2))#port
            print 'going to ',addr,port[0]
            reply = "\x05\x00\x00\x01"#ver success 00 01 ip(4) port(2)
            try:
                if protocol == 1:
                    proxyproxyRemote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    proxyproxyRemote.connect((addr, port[0]))# connection to proxyproxyRemote
                else:
                    reply = '\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00'#refuse server
                serAddress = proxyproxyRemote.getsockname()#get address and port
                print 'local:',serAddress

                reply += socket.inet_aton(serAddress[0]) + struct.pack(">H", serAddress[1])
            except socket.error:
                reply = '\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00'#refuse server
            clientProxy.send(reply)
            if reply[1] == '\x00':
                if protocol == 1:
                    fdset = [clientProxy, proxyproxyRemote]
                    id = current_thread().getName()
                    while True:
                        r, w, e = select.select(fdset, [], [])
                        if clientProxy in r:
                            data = clientProxy.recv(4096)
                            print '%s\t:from browse'%id
                            if proxyproxyRemote.send(data) <= 0: break
                        if proxyproxyRemote in r:
                            data =proxyproxyRemote.recv(4096)
                            print '%s\t:from Remote'%id
                            if clientProxy.send(data) <= 0: break


port = 1080
server = SocketServer.ThreadingTCPServer(('', port), ProxyServer)
print 'server started'
server.serve_forever()



