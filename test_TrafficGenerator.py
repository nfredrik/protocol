import unittest

from DataObject import *
from Protocol import *
from PacketGenerator import *
from PacketInterpreter import *
from TrafficGenerator import *


class TestTrafficGenerator(unittest.TestCase):
#    def test___init__(self):


    def mysetUp(self,  number):
        # Pick a data object. Could be anything, a Loopback object or a SerialPort or something else
        self.io = NewLoopDataObject()
        #io = SerialWrapper('/dev/pts/2')
        #io.start()

        # Pick a a Protocol. Make a prototype and check different techniques...
        self.protocol = LenkoProtocol(self.io)

        # make an instance of the traffic generator
        self.generator = TrafficGenerator(self.protocol,  number)

    

    def test_generateSnow(self):
        self.mysetUp(0)
        self.generator.generateSnow()
        self.assertTrue(self.generator.eventIsSet())

    def test_stopgenerateSnow(self):
        self.mysetUp(1)
        self.generator.stopgenerateSnow()
        self.assertTrue(self.generator.eventIsSet())


if __name__ == '__main__':
    unittest.main()
