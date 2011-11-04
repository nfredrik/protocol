import threading
import serial
import sys
import time

class DataObject(object):
    """Base class for Data Objects"""
    def __init(self):
       pass

    def  Write(self, buf,  bytes):
         pass

    def  signalwhenReady(self,  callback):
         self.callback = callback

#
# TODO: check how threading works i.e run()-method , simulate the serial port with socat.
#

class SerialWrapper(DataObject,  threading.Thread):
     def __init__(self, port):
         print "Running constructor in SerialWrapper"
         threading.Thread.__init__(self)
         DataObject.__init__(self)

         try:
            self.m_fh = serial.Serial(port, 38400, timeout=1)
            self.m_fh.open()
         except serial.SerialException, e:
            sys.stderr.write("Could not open serial port %s: %s\n" % (self.m_fh.portstr, e))
            sys.exit(1)

     def Write(self,  buf,  bytes):
          print 'serialWrapper:', buf
#          self.m_fh.write(buf)
          self.m_fh.write(''.join(chr(i) for i in buf))
          pass

     def run(self):
#         return
         while True:
            print "SerialWrapper, before read()"
            data = self.m_fh.read(1)              # read one, blocking
            print "SerialWrapper, after read()"
            n = self.m_fh.inWaiting()             # look if there is more
            if n:
                print ' got:', n, 'bytes'
                data = data + self.m_fh.read(n)   # and get as much as possible
            time.sleep(0.5 )
         self.callback(data,  n+1)


class LoopDataObject(DataObject):

     def  Write(self, buf,  bytes):
        self.buffer = []
        for d in buf:
            self.buffer.append(d)

        self.callback(self.buffer,  bytes)

class NewLoopDataObject(DataObject):

     def  Write(self, buf,  bytes):
#       print 'NewLoopDataobject, bytes:', bytes
        self.callback(buf,  bytes)



