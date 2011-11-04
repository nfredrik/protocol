from Packet import Packet
#
# TODO:
#

class Protocol(object):
    """Abstract class for all protocols"""
    def __init__(self,  dataObject):
        self.m_dataObject = dataObject

    def OnData(self,  data,  bytes):
        raise NotImplementedError, "Implement me"

    def connectCallback(self,  callback):
         self.callback = callback

