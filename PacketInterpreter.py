from Packet1 import *


class PacketInterpreter(object):
    def getStartProduceResponse(self, packet):
        self.isValid = (packet.size()  == 4) and (packet.getCommand() == LenkoPacket.STARTPRODUCE_RESP)
 #       print 'interpreter:',  packet.size(), packet.getCommand()
        return self.isValid
        
    def getStopProduceResponse(self, packet):
        self.isValid = (packet.size()  == 5) and (packet.getCommand() == LenkoPacket.STOPPRODUCE_RESP)
        return self.isValid        
