from Packet1 import *
#
# TODO:
#

class Protocol(object):
    """Abstract class for all protocols"""
    def __init__(self,  dataObject):
        self.m_dataObject = dataObject
        self.m_dataObject.signalwhenReady(self.NewOnData)

    def OnData(self,  data,  bytes):
        raise NotImplementedError, "Implement me"

    def connectCallback(self,  callback):
         self.callback = callback


class BinaryProtocol(Protocol):

    def Send(self, LenkoPacket):
         buffer = []
         buffer.append(0x25)
         buffer.append(lenkoPacket.getCommand())
         buffer.append(13)    # checksum

         kalle =''

         for n in buffer:
             kalle += 'B '
         k = struct.Struct(kalle)
         packed_data = k.pack(*buffer)

    def OnData(self,  data,  bytes):


         for d in data:
             r = unpack('B',  d)
#             print "we got a token:",  r

    def ResetState(self):
         pass


#
# Better enums than this. Possible to change constructor i a sub class and still have to abstract constructor in action?
#
class LenkoProtocol(Protocol):

   INVALID = 0
   STARTTOKEN = 1
   COMMAND = 2
   LENGTH = 3
   PAYLOAD = 4
   CHKSUM = 5


   def __init__(self, dataObject):
       Protocol.__init__(self, dataObject)
#       States = self.enum( INVALID = 0, STARTTOKEN = 1,COMMAND = 2, LENGTH = 3,PAYLOAD = 4, CHKSUM = 5)
       self.states = {
                      self.INVALID    : self.invalid,
                      self.STARTTOKEN :self.starttoken, 
                      self.COMMAND    : self.command, 
                      self.LENGTH     : self.length, 
                      self.PAYLOAD    : self.payload, 
                      self.CHKSUM     : self.chksum
                     }
                   

   def enum(**enums):
        return type('Enum', (), enums)

   def ResetState(self):
         self.state = self.STARTTOKEN
  
# | #   |  seq no |  | dest address  | src address | command | length (n) | payload |  chksum | """ 

        

   def Send(self,  lenkoPacket):
 
         # Build a packet!   token, command, size, payload, chksum
         self.buffer = []
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
        """this routine should be called by the data object and if it works emit a packet"""
        self.packet = LenkoPacket(254)

         # Gather the packet!   token, command, size, payload, chksum
#        print 'received data:', data
#        self.data = self.unpack(data, bytes)
        self.data = data
#        print 'received data 2nd:', self.data
        self.checksum = 0

        for self.d in self.data:

          if (self.state == self.STARTTOKEN):
              if (self.d == ord('#')):

                 self.state = self.COMMAND
              else:
                  print "no start token yet..."

          elif (self.state == self.COMMAND):
              # Fake here, turn  Request to a Response by an increment... compensate above ..
              self.d+= 1
              self.packet.setCommand(self.d)
              self.state = self.LENGTH

          elif (self.state == self.LENGTH):
              self.m_length = self.d
              self.state = self.PAYLOAD

          elif (self.state == self.PAYLOAD):
              if self.m_length:
                  self.packet.push_back(self.d)
                  self.m_length = self.m_length -1

              if not self.m_length:
                  self.state = self.CHKSUM

          elif (self.state == self.CHKSUM):
               # For now, compensate for incr from REQ to RESP, see above ...
               if (self.checksum & 255) == (self.d + 1):
                  self.callback(self.packet)
               else:
                  print 'wrong checksum, expected:', (self.checksum & 255), 'got:', self.d
          else:
              print 'wrong state:', self.state
              self.state = self.STARTTOKEN

          self.checksum+= self.d

   def NewOnData(self,  data,  bytes):
        self.packet = LenkoPacket(254)
       
        for self.d in data:
#              print 'state:', self.state
              try :
                  self.states[self.state](self.d)
              except:
                  print 'we go an invalid state',  self.state
                  self.state = self.STARTTOKEN
                  
              self.checksum+= self.d

   def invalid(self, state):
        print 'invalid'

   def starttoken(self, d):
        if ((d  >> 8) == ord('#')):
                 self.checksum = 0
                 self.state = self.COMMAND
                 print 'seqno:',  hex((d & 0xff))
        else:
                  print "no start token yet got:",  d
                  
   def command(self, d):
        # Fake here, turn  Request to a Response by an increment... compensate above ..
        # TODO: Check if it's a valid command/response ...
        self.d+= 1
        self.packet.setCommand(self.d)
        self.state = self.LENGTH
          
   def length(self, d):
        # Check if it's < than max packet size
        self.m_length = self.d
        self.state = self.PAYLOAD
         
   def payload(self, d):
        if self.m_length:
            self.packet.push_back(self.d)
            self.m_length = self.m_length -1

        if not self.m_length:
            self.state = self.CHKSUM
         
   def chksum(self, d ):
        # For now, compensate for incr from REQ to RESP, see above ...
        if (self.checksum & 255) == (self.d + 1):
            print 'we here now ...'
            self.callback(self.packet)
        else:
            print 'wrong checksum, expected:', (self.checksum & 255), 'got:', self.d
     
     
     
