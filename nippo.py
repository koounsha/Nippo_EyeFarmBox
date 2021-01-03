import serial
import socket
import json 

ser = serial.Serial('/dev/ttyUSB0',9600,timeout=None)

##################################################
# set parameter 
##################################################
# json config file read 
json_open = open('/home/pi/Documents/uecs.json', 'r')
json_load = json.load(json_open)

# CCM
CCM_name = str(json_load['CCM']['name'])
CCM_type = str(json_load['CCM']['type'])
CCM_room = str(json_load['CCM']['room'])
CCM_region = str(json_load['CCM']['region'])
CCM_order = str(json_load['CCM']['order'])
CCM_priority = str(json_load['CCM']['priority'])
CCM_ip = str(json_load['CCM']['ip_address'])

##################################################
# UECS UDP
##################################################
HOST = ''   
PORT = 16520
so =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
so.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
ADDRESS = "255.255.255.255"
def CCM_send(name,val):
    msg = "<?xml version=\"1.0\"?><UECS ver=\"1.00-E10\">"
    msg += "<DATA type=\"" + CCM_name + name + "." + CCM_type + "\""
    msg += " room=" + "\"" + CCM_room + "\""
    msg += " region=" + "\"" +  CCM_region + "\""
    msg += " order=" + "\"" +  CCM_order + "\""
    msg += " priority=" + "\"" +  CCM_priority + "\">"
    msg += str(val) + "</DATA>"
    msg += "<IP>" + CCM_ip + "</IP></UECS>"
    print(msg)
    so.sendto(msg, (ADDRESS, PORT))
    #wdt.feed()

##################################################
# Sensor Function
##################################################

while True:
  s = ser.readline()
  l = s.split(',')

  if len(l)>0:
    tmp0 = round(int(float(l[4])) * 0.1,2)
    tmp1 = round(int(float(l[5])) * 0.1,2)
    hum  = round(int(float(l[13])),2)
    hd   = round(int(float(l[14])),2)
    dew  = round(int(float(l[15])) * 0.1,2)
    sv   = round(int(float(l[16])) * 0.1,2)
    ah   = round(int(float(l[17])) * 0.1,2)
    co2  = round(int(float(l[18])),2)
    insolation = (int(float(l[29])))
   
  if tmp0>0 and tmp0>0 and hd>0 and dew>0 and sv>0 and ah>0 and co2>0:
    d = {'_nippo_temp0': tmp0, '_nippo_temp1': tmp1, '_nippo_hum':hum ,'_nippo_hd':hd ,'_nippo_dew':dew ,'_nippo_sv':sv ,'_nippo_ah':ah ,'_nippo_co2':co2 ,'_nippo_insolation':insolation}
    
    for k, v in d.items():
      CCM_send(k,v)


ser.close()
