#              .';:cc;.
#            .,',;lol::c.
#            ;';lddddlclo
#            lcloxxoddodxdool:,.
#            cxdddxdodxdkOkkkkkkkd:.
#          .ldxkkOOOOkkOO000Okkxkkkkx:.
#        .lddxkkOkOOO0OOO0000Okxxxxkkkk:
#       'ooddkkkxxkO0000KK00Okxdoodxkkkko
#      .ooodxkkxxxOO000kkkO0KOxolooxkkxxkl
#      lolodxkkxxkOx,.      .lkdolodkkxxxO.
#      doloodxkkkOk           ....   .,cxO;
#      ddoodddxkkkk:         ,oxxxkOdc'..o'
#      :kdddxxxxd,  ,lolccldxxxkkOOOkkkko,
#       lOkxkkk;  :xkkkkkkkkOOO000OOkkOOk.
#        ;00Ok' 'O000OO0000000000OOOO0Od.
#         .l0l.;OOO000000OOOOOO000000x,
#            .'OKKKK00000000000000kc.
#               .:ox0KKKKKKK0kdc,.
#                      ...
#
# Author: peppe8o
# Date: Jul 24th, 2022
# Version: 1.0
# https://peppe8o.com

import network, rp2
import time

def connectWiFi(ssid,password,country):
   rp2.country(country)
   wlan = network.WLAN(network.STA_IF)
   wlan.config(pm = 0xa11140)
   wlan.active(True)
   wlan.connect(ssid, password)
   # Wait for connect or fail
   max_wait = 10
   while max_wait > 0:
      if wlan.status() < 0 or wlan.status() >= 3:
        break
      max_wait -= 1
      print('waiting for connection...')
      time.sleep(1)

   # Handle connection error
   if wlan.status() != 3:
      raise RuntimeError('network connection failed')
   else:
      print('connected')
      status = wlan.ifconfig()
      print( 'ip = ' + status[0] )
   return status
