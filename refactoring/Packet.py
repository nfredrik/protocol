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
            raise Exception('Nothing to pop')
            
        return self.m_Vector.pop(0) # pop first element. Default last element

    def push_back(self, byte):
        if self.size() > self.m_maxPacketsize:
            raise Exception('Exceeded max size')
            
        self.m_Vector.append(byte)

    def size(self):
         return len(self.m_Vector)



