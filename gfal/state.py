#!/usr/bin/env python

import pythonpath
import gfal
import time
import re
import sys
from string import strip

'''
Dit script fiets door een file genaamd "files" heen om de status op te vragen
van een file. 

ONLINE              betekent dat de file alleen op disk staat
NEARLINE            betekent dat de file alleen op tape staat
ONLINE_AND_NEARLINE betekent dat de file op disk en op tape staat

Verder is dit script verre van netjes.

De filenamen in "files" hebben de vorm van:

/pnfs/grid.sara.nl/data/.....

Enjoy!!!

Ron
'''

m=re.compile('/pnfs')
nf=100

f=open('files','r')
urls=f.readlines()
f.close()

surls=[]
for u in urls:
    surls.append(m.sub('srm://srm.grid.sara.nl:8443/srm/managerv2?SFN=/pnfs',strip(u)))

mx=len(surls)

i=0
while i<mx:
    req={}
    mxi=min(i+nf,mx)
    s=surls[i:mxi]
    req.update({'surls':s})
    req.update({'setype':'srmv2'})
    req.update({'no_bdii_check':1})
    req.update({'srmv2_lslevels':1})
    req.update({'protocols':['gsiftp']})
    a,b,c=gfal.gfal_init(req)
    a,b,c=gfal.gfal_ls(b)
    a,b,c=gfal.gfal_get_results(b)
    for j in range(0,len(c)):
       print c[j]['surl']+" "+c[j]['locality']
    i=i+nf
    time.sleep(1)
