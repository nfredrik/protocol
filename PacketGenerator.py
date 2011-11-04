from Packet1 import *

class PacketGenerator(object):
    def __init__(self):
        pass

    def  generateStartProcedure(self):
        self.p = LenkoPacket(254)
        self.p.setCommand(LenkoPacket.STARTPRODUCE_REQ)
        payload = [25, 26, 27, 28]
        for p in payload:
            self.p.push_back(p)

        return self.p

    def  stopProcedure(self):
        self.p = LenkoPacket(4)
        self.p.setCommand(LenkoPacket.STOPPRODUCE_REQ)
        payload = [37, 38, 39, 40,  41]
        for p in payload:
            self.p.push_back(p)

        return self.p
