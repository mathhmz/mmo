import sys
import protocol
from twisted.python import log
from twisted.internet import reactor, task
from autobahn.twisted.websocket import  WebSocketServerFactory

class GameFactory(WebSocketServerFactory):
    def __init__(self, hostname, port):
        self.protocol = protocol.GameServerProtocol
        super().__init__(f"ws://{hostname}:{port}")
        
        self.players: set[protocol.GameServerProtocol] = set()
        
        
        tickloop = task.LoopingCall(self.tick)
        tickloop.start(1 / 20) 
        
    def tick(self):
        for p in self.players:
            p.tick()
            
    #override
    
    def buildProtocol(self, address):
        p = super().buildProtocol(address)
        self.players.add(p)
        return p
    
if __name__ == '__main__':
    log.startLogging(sys.stdout)
    
    PORT: int = 8081
    factory = GameFactory("0.0.0.0", PORT)
    
    
    reactor.listenTCP(PORT,factory)
    reactor.run()