import string
import sys

rclocal=open('/etc/rc.local','r')
mounted=False
exitstatus=1
mdata=[]

for line in rclocal:
    if '#' not in line and len(line) > 2 and 'cifs' in line:
       (rctype,rcmount,rcpass,rcoption,rcmdd)=[0,0,0,0,0]
       if len(line.split()) == 4:
          (rctype,rcmount,rcpass,rcoption)=line.strip().split()
       if len(line.split()) == 5:
          (rctype,rcmount,rcpass,rcoption,rcmdd)=line.strip().split()

       procmounts_content=open('/proc/mounts','r')
       for pc in procmounts_content:
           if '#' not in pc and len(pc) > 2 and 'cifs' in pc:
             if len(pc.split()) == 6:
               (pcmount,pcpass,pctype,pcoption,pcmdd,pcmcc)=pc.strip().split()
               if pctype in  rctype and rcpass == pcpass:
                  #print "Mount OK !", rctype, pcpass , rcpass
                  mounted=True

       procmounts_content.close()

       if mounted:
          exitstatus=0
          mdata.append(rcpass)
          #print "Check Mount ",rctype , rcpass , mounted
       else:
          exitstatus=1
          mdata.append(0)
          print "Mount not OK :-( "
          sys.exit(exitstatus)
       mounted=False

print mdata
sys.exit(exitstatus)

