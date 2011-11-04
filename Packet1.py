#
# TODO: push_pack, add control for size of vector  if self.maxPacketsize < len(m_Vector) : ...
#
from Protocol import *

class Packet(object):
    """ Abstract class for packets"""
    def __init__(self,  maxPacketSize):
        self.m_maxPacketsize =  maxPacketSize
        self.m_Vector = []

    def AddByte(self,  byte):
        self.m_Vector.append(byte)

    def GetByte(self):
         self.m_Vector;

    def pop(self):
        if self.size() == 0:
            raise NameError
            
        return self.m_Vector.pop(0) # pop first element. Default last element

    def push_back(self, byte):
        if self.size() > self.m_maxPacketsize:
            raise NameError
            
        self.m_Vector.append(byte)
#         print ' size now:' , len(self.m_Vector)

    def size(self):
         return len(self.m_Vector)

class LenkoPacket(Packet):
    """ Packet layout, all fields one byte
          | start token  == '#' | addr | command | errorcode | length | payload | chksum | """
    # Commands/Requests and Replies/Responses
    STARTPRODUCE_REQ = 1
    STARTPRODUCE_RESP = 2
    STOPPRODUCE_REQ   = 3
    STOPPRODUCE_RESP   = 4

    ADDR = 18

#    def __init__(self):
#        Packet(254)

    def setCommand(self,  command):
        self.m_Command = command

    def  getCommand(self):
       return self.m_Command

    def getStartTokenReq(self):
       return ord('#')

    def getStartTokenResp(self):
       return ord('%')


class LenkoPacketResponse(Packet):
        """ Packet layout, all fields one byte. Header fixed to 5 bytes. length comprises
              payload and checksum
          | start token  == '%' | addr | response | errorcode | length | payload | chksum | """



