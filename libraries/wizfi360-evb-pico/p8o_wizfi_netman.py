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

from machine import UART, Pin
import time

# WizFi360 settings for WizFi360-EVB-Pico board
PORT = 1
RX = 5 
TX = 4
resetpin = 20
rtspin = False

# UART communication initialization
uart = UART(PORT, 115200, tx= Pin(TX), rx= Pin(RX), txbuf=1024, rxbuf=1024*2)

def UARTcomm(command, retry=3): # This controls one UART command exection
    timeout = 5000
    try_id = 0
    uart.write(command + '\r\n')
    return_line = b''
    start = time.ticks_ms()
    try:
        while not "OK" in return_line:
            while not uart.any():
                if time.ticks_diff(time.ticks_ms(), start) > timeout: return "Timeout error!"
                pass
            resp = uart.readline()
            return_line = return_line + resp
        result = return_line.decode('utf-8').strip('\r\n')
        if try_id > 0: print("Warning: tried " + try_id + " times, but this could not be a problem...")
        return result
    except:
        pass

def scanAP(): # Scans the available Access Points and prints the related list
    enc=["OPEN","WEP","WPA_PSK","WPA2_PSK","WPA_WPA2_PSK","WPA2_ENTERPRISE","WPA3_PSK","WPA2_WPA3_PSK","WAPI_PSK"]
    scan=UARTcomm("AT+CWLAP")
    AccessPoints = []
    for line in scan.split("\r\n"):
      if line[0:8] == "+CWLAP:(":
        AccessPoint = line[8:-1].split(",")
        for i, val in enumerate(AccessPoint):
            AccessPoint[i] = str(val)
            try:
                AccessPoint[i] = int(AccessPoint[i])
            except ValueError:
                AccessPoint[i] = AccessPoint[i].strip('"')
        AccessPoints.append(AccessPoint)
    print("List of available APs:\r\n")
    for ap in AccessPoints:
        print("SSID:                        "+ap[1])
        print("Encryption Method:           "+enc[ap[0]])
        print("Signal strength:             "+str(ap[2]))
        print("AP MAC Address:              "+ap[3])
        print("Channel Number:              "+str(ap[4]))
        print("WPS (0-disabled, 1-enabled): "+str(ap[5]))
        print("\r\n")
        
def APconnect(ssid,pwd): # Connects to WiFi
    print("Connecting to WiFi:")
    result=UARTcomm('AT+CWJAP_CUR="'+ssid+'","'+pwd+'"')
    print(result)

    print("Retrieving IP and Mac Address:")
    set_cmd=UARTcomm("AT+CIFSR")
    for line in set_cmd.split("\r\n"):
        if line[0:13] == "+CIFSR:STAIP,": ip=line[14:-1]
        if line[0:14] == "+CIFSR:STAMAC,": mac=line[15:-1]
    return ip,mac

def ping_test(dest): # performs a PING test
    ping_result = UARTcomm('AT+PING="'+dest+'"')
    res = ping_result.split("\r\n")
    res_len = len(res)
    if res[res_len-1] == "OK":
        res_time = [idx for idx in res if idx.startswith('+')]
        print("Ping test to " + dest + " successful.")
        print("Response get in " + res_time[0] + " milliseconds")
        return
    else:
        print("Ping test to " + dest + " failed!")
        return



# ************************** MQTT SETUP ****************************

def mqtt_userinfo_config(username: str, password: str, client_id: str, keep_alive: int) -> bool:
    """Set the configuration of MQTT connection. """
    mqtt_cfg = UARTcomm("AT+MQTTSET=" + '"' + str(username) + '","' + str(password) + '","' + str(client_id) + '",' + str(keep_alive))
    res = mqtt_cfg.split("\r\n")
    res_len = len(res)
    if res[res_len-1] == "OK":
        print("MQTT user info set")
        return True
    else:
        print("Error occurred setting MQTT user info")
        return False

def mqtt_set_topic(publish_topic: str, sub_topic: str) -> bool:
    """ Registers a MQTT topics."""

    mqtt_set_topic = UARTcomm("AT+MQTTTOPIC=" + '"'+str(publish_topic)+ '","' + str(sub_topic)+ '"')
    res = mqtt_set_topic.split("\r\n")
    res_len = len(res)
    
    if res[res_len-1] == "OK":
        print("Registered on topic "+publish_topic)
        return True
    else:
        print("Error occurred registering on topic "+publish_topic)
        return False

def mqtt_connect(auth_enable:int, broker_ip: str, broker_port: int, link_id: Optional[int] = None) -> bool:
    """Initiates connection with the MQTT Broker."""
    
    if not link_id:
        mqtt_con = UARTcomm("AT+MQTTCON=" + str(auth_enable) + ',"' + str(broker_ip) + '",' + str(broker_port))
    else:
        mqtt_con = UARTcomm("AT+MQTTCON=" + str(link_id) + "," + str(auth_enable) + ',"' + str(broker_ip) + '",' + str(broker_port))
    
    res = mqtt_con.split("\r\n")
    res_len = len(res)
    if res[res_len-1] == "OK":
        print("Connected to Broker " + broker_ip)
        return True
    else:
        print("Error occurred connecting to Broker " + broker_ip)
        return False

def mqtt_publish(message: bytes) -> bool:
    """Publishes a message to a topic provided."""

    mqtt_pub =  UARTcomm("AT+MQTTPUB=" + '"' + str(message) + '"')
    res = mqtt_pub.split("\r\n")
    res_len = len(res)
    
    if res[res_len-1] == "OK":
        print("Message: "+message+" sent")
        return True
    else:
        print("Error occurred sending message "+message)
        return False

def mqtt_disconnect() -> bool:
    """ Disconnects the MiniMQTT client from the MQTT broker."""        
    mqtt_disc =  UARTcomm("AT+MQTTDIS")
    res = mqtt_disc.split("\r\n")
    res_len = len(res)
    
    if res[res_len-1] == "CLOSE":
        print("Disconnected from MQTT broker")
        return True
    else:
        return False
    
