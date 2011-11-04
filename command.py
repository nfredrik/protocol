#!/usr/bin/env python

import time

if __name__ == '__main__':

     pipe = open('/dev/pts/2', 'w')
     cntr = 1000000

     while --cntr > 0:
         time.sleep(1)
         nisse =pipe.read()
         print 'we got:', nisse
         pipe.flush()
