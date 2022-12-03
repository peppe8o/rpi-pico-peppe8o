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
# Date: Dec 2nd, 2022
# Version: 1.0
# blog: https://peppe8o.com

import p8o_wizfi_netman as nm

# WiFi connection settings
(ssid,pwd)="Voyager-1","7ville7ville"

print("Testing AT command:")
print(nm.UARTcomm("AT")) # simple AT command test

#sys.exit()

print("Configuring Station Mode:")
print(nm.UARTcomm("AT+CWMODE_CUR=1")) # Set to Station Mode

print("Scanning Access Points:")
nm.scanAP()

print()
ip,mac=nm.APconnect(ssid,pwd)
print("IP Address = "+ip)
print("MAC Address = "+mac)

print()
print("Performing simple ping command to IP:")
nm.ping_test("8.8.8.8")

print()
print("Performing ping command to domain:")
nm.ping_test("www.google.com")

print()
print("Performing ping command to wrong domain:")
nm.ping_test("saacss.com") # ping wrong domain


print()
print("Performing MQTT send test")

# MQTT settings
mqtt_server = '192.168.1.91'
client_id = 'PicoW'
user_t = 'pico'
password_t = 'giuseppe'
topic_pub = 'hello'
SUBSCRIBE_TOPIC = 'hello' # can be same as topic_pub
mqtt_port = 1883
auth = 0
keep_alive = 300

# MQTT message to send
message="Hello from Peppe8o.com!"

# MQTT setup
nm.mqtt_userinfo_config(user_t, password_t, client_id,keep_alive)
nm.mqtt_set_topic(topic_pub, SUBSCRIBE_TOPIC)
nm.mqtt_connect(auth, mqtt_server, mqtt_port)

# MQTT publishing
nm.mqtt_publish(message)

#MQTT disconnection
nm.mqtt_disconnect()
