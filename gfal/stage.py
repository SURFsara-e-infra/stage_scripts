#!/usr/bin/env python

import pythonpath
import gfal
import time
import re
import sys
from string import strip
'''
Dit script fiets door een file genaamd "files" heen om die te stagen van tape.
Verder is dit script verre van netjes.

Je kunt ook de pin lifetime opgeven in "srmv2_desiredpintime" in seconden. 

De filenamen in "files" hebben de vorm van:

/pnfs/grid.sara.nl/data/.....

Enjoy!!!

Ron
'''

m=re.compile('/pnfs')

f=open('files','r')
urls=f.readlines()
f.close()

surls=[]
for u in urls:
    surls.append(m.sub('srm://srm.grid.sara.nl:8443/srm/managerv2?SFN=/pnfs',strip(u)))


req={}

# Zet de timeout op 72 uur
#
# Uit de man page:
# gfal_set_timeout_srm  Sets  the  SRM  timeout, used when doing an asyn-
# chronous SRM request. The request will be aborted if it is still queued
# after ??? seconds.
gfal.gfal_set_timeout_srm(259200)

req.update({'surls':surls})
req.update({'setype':'srmv2'})
req.update({'no_bdii_check':1})
req.update({'protocols':['gsiftp']})

#Zet de tijd dat de file op disk gepinned blijft op een week
req.update({'srmv2_desiredpintime':604800})

returncode,object,err=gfal.gfal_init(req)
if returncode != 0:
        sys.stderr.write(err+'\n')
        sys.exit(1)

returncode,object,err=gfal.gfal_prestage(object)
if returncode != 0:
    sys.stderr.write(err+'\n')
    sys.exit(1)
del req
