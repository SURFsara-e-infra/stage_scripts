#!/usr/bin/env python

import gfal2
import time
import re
import sys
import json
from string import strip
'''
Dit script fiets door een file genaamd "files" heen om die te stagen van tape.
Verder is dit script verre van netjes.

Je kunt ook de pin lifetime opgeven in "pintime" in seconden. 

De filenamen in "files" hebben de vorm van:

/pnfs/grid.sara.nl/data/.....

Enjoy!!!

Ron
'''

hour=3600
day=24*hour
week=7*day

m=re.compile('/pnfs')

f=open('files','r')
urls=f.readlines()
f.close()

surls=[]
for u in urls:
    surls.append(m.sub('srm://srm.grid.sara.nl:8443/srm/managerv2?SFN=/pnfs',strip(u)))


req={}

# Zet de timeout
timeout=72*hour

#Zet de tijd dat de file op disk gepinned blijft 
pintime=4*day

f=open('requests.json','w')

for surl in surls:
    ctx=gfal2.create_context()
    try:
        # bring_online(surl, pintime, timeout, async)
        (status,token)=ctx.bring_online(surl,pintime,timeout,True)

        d={'surl':surl,'token':token}
        j = json.dumps(d, indent=4)
        print >> f,j
    except gfal2.GError, e:
        print "Could not bring the file online:"+surl+" "
        print "\t", e.message
	print "\t Code", e.code

f.close()
