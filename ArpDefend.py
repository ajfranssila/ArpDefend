#!/usr/bin/env python
import os
import re
from subprocess import Popen, PIPE

IP = "SYÖTÄ IP"

#pingaa gatewayta
pingi = os.system("ping -c 1 " + IP)
if pingi != 0:
   print "ei yhteytta gatewayhin, lopetetaan"
   exit()

#selvittaa gatewayn macin arp cachesta
pid = Popen(["arp", "-n", IP], stdout=PIPE)
s = pid.communicate()[0]
mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0]

print("gatewayksi maaritetty: " + IP + ", jonka MAC osoite on: " + mac)
print("kaynnistetaan ARP valvonta!")

#Lukee arp cachea loopilla. Jos muutos gatewayn osalta, soittaa halytysaanen ja ilmoittaa spoofingista.
while True:
   pid = Popen(["arp", "-n", IP], stdout=PIPE)
   s = pid.communicate()[0]
   mac2 = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0]
   if mac2 != mac:
      print "\a"
      print("ARP spoofing havaittu!!!")
      break
print("ARP valvonta suljetaan!")