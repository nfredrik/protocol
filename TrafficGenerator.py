
from DataObject import *
from Protocol import *
from PacketGenerator import *
from PacketInterpreter import *

import sys
import struct
import binascii

import threading


import time


## http://www.doughellmann.com/PyMOTW/struct/index.html#module-struct


# TODO : Figure out how to doi this in a unit test maner
#
#

class TrafficGenerator(object):
    def __init__(self, protocol,  number):
         self.m_protocol = protocol
         self.m_protocol.connectCallback(self.signalOnPacket)
         self.m_interpret = PacketInterpreter()
         self.m_gen = PacketGenerator()
         self.event = threading.Event()
         self.m_packetCounter = number


    def generateSnow(self):
         self.query  = self.m_gen.generateStartProcedure()
         self.event.clear()
         self.m_protocol.ResetState()
         self.m_protocol.Send(self.query)
         self.event.wait(3)
         # Give the key to the dict ...
       
         
    def stopgenerateSnow(self):    
         self.query = self.m_gen.stopProcedure()
         self.event.clear()
         self.m_protocol.ResetState()
         self.m_protocol.Send(self.query)
         self.event.wait(3)
         # Give the key to the dict ...
  

    def signalOnPacket(self,  packet):


         # make dict to pick the right routine to call ....
         if  self.m_packetCounter == 0:
             if (self.m_interpret.getStartProduceResponse (packet)):
                 self.event.set()
             else:
                 print "we got an invalid packet, not startprocedure response!!"

         elif  self.m_packetCounter == 1: 

          if (self.m_interpret.getStopProduceResponse(packet)):
                 self.event.set()
          else:
                 print "we got an invalid packet, not stopprocedure response!!"

    def eventIsSet(self):
          return self.event.isSet()    



