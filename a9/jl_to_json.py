'''
Created on Nov 13, 2017

@author: anand
'''

import json
from os import linesep

fname = 'sof.jl'
fop = open('json_sof.json','wb')
fop.write('[')
with open(fname,'rb') as f:
    for line in f:
        fop.write( line +','+ linesep)

fop.write(']')
fop.close()

print 'Done'