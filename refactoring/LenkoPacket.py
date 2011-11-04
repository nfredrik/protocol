from Packet import Packet

class LenkoPacket(Packet):
    """ Packet layout, all fields one byte
          | CHR_START  == 0xeb, 1 byte |
          | Packet ID , Not included in examples ..., 1 byte|
          | Address Identifier, 1 byte | 
          | Address list field, dynamic |
          | Data field, dynamic |
          | CHR_END == 0xed """
    # Commands
    PT_CMD_DATA = 0x2001


    # Replies 
    PT_DATA_TEMP_RHBAR = 0x3010
    PT_DATA_WIND = 0x3011

    CHR_START = 0xeb

#    def __init__(self):
#        Packet(254)

    def setpacketId(self,  id):
        self.m_packetId = id

    def setNoOfAddr(self, no):
        self.m_noOfAddr = no & 0x07

    def getNoOfAddr(self, no):
        return self.m_noOfAddr

    def setCurrAddrPos(self, pos):
        self.m_currAddrPos = (pos & 0x38) >> 3

    def setFullAddr(self, full):
        self.m_fullAddr = ((full & 0x40) == 0x40)

    def setReversedAddr(self, rev):
        self.m_revAddr = (rev & 0x80) == 0x80

    def setAddrField(self, elem):
        self.m_addrList.append(elem)

    def setValidationType(self, s):
        self.m_validtype = s

    def getValidation16bit(self, s):
        return (self.m_validtype == 2)



    def  getCommand(self):
       return self.m_Command

    def checkChrStart(self, data):
       return (CHR_START == data)

    def getChrStart(self, data):
       return CHR_START

    def getChrEnd(self):
       return 0xed

    def getChrCRC(self):
       return 0xec


class LenkoPacketResponse(Packet):
        """ Packet layout, all fields one byte. Header fixed to 5 bytes. length comprises
              payload and checksum
           """
