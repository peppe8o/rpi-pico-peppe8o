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
# Date: Aug 17th, 2022
# Version: 1.0
# https://peppe8o.com

import netman
import os, socket

country = 'IT'
ssid = 'MyWiFiAccessPoint'
password = 'MyWiFiPassword'

#web server basic settings
public_folder='/public_html'
index_page='/index.html'
not_found_page='/notfound.html'

wifi_connection = netman.connectWiFi(ssid,password,country)

def path(request):
    decoded_req = request.decode()
    get_req = decoded_req.partition('\n')[0]
    path = get_req.split(" ")[1]
    path=path.rsplit('/', 1) #path[0]->folder, path[1]->filename
    path[1]='/'+path[1]
    return path

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #avoids errors for address in use on reconnection
s.bind(addr)
s.listen(1)

print('listening on', addr)

# Listen for connections
while True:
  try:
    cl, addr = s.accept()
    print('client connected from', addr)
    request = cl.recv(1024)
    
    url=path(request)
    if url[0]=="" and url[1]=="/": url[1] = index_page
    print(url)
    
    if url[1][1:] not in os.listdir(public_folder+url[0]):
        url[0]=''
        url[1]=not_found_page
        header='HTTP/1.0 404 Object Not Found\r\n\r\n'
    else:
        header='HTTP/1.0 200 OK\r\n\r\n'

    f = open(public_folder+url[0]+url[1], 'r')
    response = f.read()
    f.close()

    cl.send(header+response)
    cl.close()

  except OSError as e:
    cl.close()
    print('connection closed')