import random
import sys

offset=0
if len(sys.argv) > 1:
    offset = int(sys.argv[1])

for ii in range(2000):
    print("Set Key:%d %d" % (offset+ii,int(10000*random.random())))