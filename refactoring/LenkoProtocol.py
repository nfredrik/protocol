from Protocol import Protocol

#
# Better enums than this. Possible to change constructor 
# i a sub class and still have to abstract constructor in action?
#
class LenkoProtocol(Protocol):

   INVALID = 0
   STARTTOKEN = 1
   VALIDATIONTYPE = 2
   PACKETNUMBER = 3
   PACKETID = 4
   ADDRSPEC = 5
   ADDRFIELD = 6
   DATALEN = 7
   DATAFIELD = 8
   WAITCRC = 7
   CRC = 8

   def __init__(self, dataObject):
       Protocol.__init__(self, dataObject)
       self.states = {
                      self.INVALID         : self.invalid,
                      self.STARTTOKEN      : self.starttoken, 
                      self.VALIDATIONTYPE  : self.validationtype,                      
                      self.PACKETNUMBER    : self.packetnumber,
                      self.PACKETID        : self.packetid, 
                      self.ADDRSPEC        : self.addrspec, 
                      self.ADDRFIELD       : self.addrfield, 
                      self.DATALEN         : self.datalen
                      self.DATAFIELD       : self.datafield
                      self.WAITCRC         : self.waitcrc
                      self.CRC             : self.crc
                     }
                   

   def enum(**enums):
        return type('Enum', (), enums)

   def ResetState(self):
         self.state = self.STARTTOKEN
  
   def addrInList(self, a):
        return (a << 0)

   def Send(self,  lenkoPacket):
 
         # Build a packet!
         self.buffer = []
         self.buffer.append(lenkoPacket.getChrStart())
         self.buffer.append(0x02)  # Validation type is 16 bit chksum
         self.buffer.append(0x01)  # Packet number
         self.buffer.append( self.addrInList(2) | self.addrInList(2))  # address type = 32bit, current addr idx, 2 addr in list 
         self.buffer.append(0x01000000)   # Addr #1
         self.buffer.append(0x078563412)  # Addr #2
         self.buffer.append(0x04000120)  # Data record  size = 4, PT_CMD_DATA

         self.buffer.append(lenkoPacket.getStartTokenReq() << 8  |  0xee )     # start token and sequence number 
         self.buffer.append(lenkoPacket.getCommand())
         self.buffer.append(lenkoPacket.size())

         for  data in range(lenkoPacket.size()):
             self.buffer.append(lenkoPacket.pop())    # pop first element

         # Calculate checksum
#         self.buffer.append(13)    # checksum
         self.buffer.append( self.CalcChkSum(self.buffer))
#         print 'checksum:', self.CalcChkSum(self.buffer)

#         print self.altpack(self.buffer)
#         print 'buffer:', self.buffer
#         self.buffer = self.pack(self.buffer)

         #    self.checksum = binascii.hexlify(unpack('B',  self.buffer[i]))

#         print 'sent data:', self.buffer
         self.m_dataObject.Write(self.buffer, len(self.buffer))

   def altpack(self, buf):
        self.togheter =  ' '.join(chr(i) for i in buf)
        print 'altpack:', self.togheter
        print 'altpack1:', self.togheter.split(' ')

   def pack(self, buf):

         kalle =''
         for n in buf:
             kalle += 'B '
         k = struct.Struct(kalle)
#         print 'kalle', kalle
         self.packed_data = k.pack(*buf)
#         print'pack, packed data:',  self.packed_data
         return self.packed_data

   def unpack(self, buf, bytes):
#         print 'unpack buf:', buf
         kalle =''
         for n in buf:
             kalle += 'B '
         k = struct.Struct(kalle)

#         print 'tjohej:', kalle

         self.unpacked_data = k.unpack(buf)
#         print'unpacked data:',  self.unpacked_data
         return self.unpacked_data

   def altunpack(self, buf):
        return buf.split(' ')


   def CalcChkSum(self, buf):
         chksum = 0
         for d in buf:
             chksum+=d
         return (chksum & 255)


   def OnData(self,  data,  bytes):
        self.packet = LenkoPacket(254)
       
        for self.d in data:
#              print 'state:', self.state
              try :
                  self.states[self.state](self.d)
              except:
                  print 'wet go an invalid state',  self.state
                  self.state = self.STARTTOKEN
                  
              self.checksum+= self.d

   def invalid(self, state):
        print 'invalid state'

   def starttoken(self, d):
        if (checkChrStart(d)):
                 self.checksum = 0
                 self.state = self.VALIDATIONTYPE
        else:
                 print "no start token yet, got:",  d
                  
   def validationtype(self, d):
       self.packet.setValidationType(self.d)
       self.state = self.PACKETNUMBER
                      
   def packetnumber(self, d):
       self.packet.setPacketNumber(self.d)
       self.state = self.ADDRSPEC

          
   def addrspec(self, d):
       self.packet.setNoOfAddr(d)
       self.packet.setCurrAddrPos(d)
       self.packet.setFullAddr(d)
       self.packet.setReversedAddr(d)
  
       self.firstaddr = True    
       self.state = self.ADDRFIELD
         
   def addrfield(self, d):

        if self.firstaddr:
            self.firstaddr = False
            if packet.getFullAddr():
                self.noOfAddrBytes = 4 * self.getNoOfAddr()
            else:
               self.noOfAddrBytes = 2 * self.getNoOfAddr()

        self.noOfAddrBytes = self.noOfAddrBytes -1
        
        if self.noOfAddrBytes:
            self.addr = d << self.noOfAddrBytes
        else:
            self.packet.setAddrField(self.addr)

        self.state = self.DATALEN

   def datalen(self, d):
       self.len = d
        self.state = self.DATA

   def data(self, d):
       # TODO: How to handle more than one data record, list in lists possible? 
       if self.len > 0:
          self.len = self.len -1 
          self.list = data
       else:
          self.state = self.WAITCRC

   def waitcrc(self, d):

       if not getChrCRC(d):
          # More data records!
          self.len = d
          self.state = self.DATA
       else:
          self.crclen = 3;
          self.state = self.CRC

   def crc(self, d):
       if getValidation16bit(d) and 
          self.crclen == 0:
          self.crclen = 1
          return

       self.crclen =  self.crclen - 1

       if self.crclen == 0:
          self.callback(self.packet)
     
     
     
