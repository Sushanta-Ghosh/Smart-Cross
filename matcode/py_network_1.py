#py_network.py is the script used to communicate with other vehicles in intersection
#This script utilizes the MQTT protocol for networking using the paho-mqtt python library
#Broker used for the operations was iot.eclipse.org, each vehicle has this script running during operation

import paho.mqtt.client as mqtt #import the client1
import time
import scipy.io as sio

channel_list = ["camera/distance/V1", "camera/distance/V2","command/V2", "command/V1"]
data_list = ['self_distance', 'v2_distance', 'v2_cmd', 'self_cmd', 'offset_theta', 'sensor_distance']
print("I am starting")

########################################
#function callback for when client vehicle connects to the broker
def on_connect(client, userdata, flags, rc):
    print("trying to connect")
    print("result = ", rc)
    if rc == 0:
        print("I am connected")
        client.connected_flag = True
        #subscribe to all necessary communication topics
        client.subscribe([("camera/distance/V1", 0),("camera/distance/V2", 0), ("command/V2", 0), ("command/V1", 0)])
    else:
        client.connected_flag = False
########################################

########################################
def on_disconnect(client, userdata, message):
    print("Disconnected from Broker")
    client.connected_flag = False
    #client.loop_stop() #stop the loop
########################################

#######################################
def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed to topics")
#######################################

########################################
def on_unsubscribe(client, userdata, message):
    print("unsubscribed from topics")
########################################

########################################
def on_publish(client, userdata, message):
    m = message;
########################################

########################################
#callback for when a message has been published regarding Vehicle 2 distance (for V1 script) and Vehicle 1 distance (for V2 script) 
def on_v2_distance(client, userdata, message):
    #print("message received " ,message.payload)
    #print("message topic=",message.topic)
    #py_data.set_data(1, float(message.payload))
    while True:
        try:
            py_data = sio.loadmat('py_data.mat')
            print("V2_distance = ", py_data['v2_distance'][0,0])
            if not(py_data['v2_distance'][0,0] == float(message.payload)):
                print("V2_distance changed = ", float(message.payload))
                data_stripped = {data_list[0]: float(py_data[data_list[0]][0,0]),
                                 data_list[1]: float(message.payload),
                                 data_list[2]: float(py_data[data_list[3]][0,0]),
                                 data_list[3]: float(py_data[data_list[3]][0,0])}
                #py_data['v2_distance'][0,0] = float(message.payload) #gives numerical value
                sio.savemat('py_data.mat',data_stripped)
            break
        except Exception:
            time.sleep(0.01)
########################################

########################################
#callback for when a message has been published regarding Vehicle 2 cmd
def on_v2_cmd(client, userdata, message):
    #print("message received " ,message.payload)
    #print("message topic=",message.topic)
    while True:
        try:
            py_data = sio.loadmat('py_data.mat')
            print("V2_cmd = ", py_data['v2_cmd'][0,0] )
            
            if not(py_data['v2_cmd'][0,0] == float(message.payload)):
                print("V2_cmd changed = ", float(message.payload))
                data_stripped = {data_list[0]: float(py_data[data_list[0]][0,0]),
                                 data_list[1]: float(py_data[data_list[1]][0,0]),
                                 data_list[2]: float(message.payload),
                                 data_list[3]: float(py_data[data_list[3]][0,0])}
                #print(data_stripped)
                sio.savemat('py_data.mat',data_stripped)
            break
        except Exception:
            time.sleep(0.01)
########################################

########################################
#callback for when a message has been published regarding Vehicle 1 distance (for V1 script) and Vehicle 2 (for V2 script) distance -ASSUME this is an acknowlegment
def on_self_distance(client, userdata, message):
    #print("message received " , message.payload);    
    #print("message topic=",message.topic)
    test = 0
    #py_data.set_data(3, float(message.payload))
########################################

########################################
#callback for when a message has been published regarding Vehicle 1 Cmd (for V1 script) and Vehicle 2 Cmd (for V2 script) -ASSUME this is an acknowlegment 
def on_self_cmd(client, userdata, message):
    test = 0
    #print("message received " ,message.payload)
    #print("message topic=",message.topic)
    #py_data.set_data(5, float(message.payload))
########################################

def on_message(client, userdata,message):
    x = message.payload
    
########################################
def on_log(client, userdata, level, buf):
    print("received log info")
########################################

########################################
def send_msg(py_data):
    #print(py_data)    
    data_stripped = {data_list[0]: float(py_data[data_list[0]]),
               data_list[1]: float(py_data[data_list[1]]),
               data_list[2]: float(py_data[data_list[2]]),
               data_list[3]: float(py_data[data_list[3]])}
    #print(data_stripped[data_list[3]])                
    client.publish(channel_list[0],data_stripped[data_list[0]])
    client.publish(channel_list[3],data_stripped[data_list[3]])
########################################

broker_address = "iot.eclipse.org"


client = mqtt.Client("V1") #create new instance

client.connected_flag = False

#client.message_callback_add("camera/distance/V1", on_self_distance)
client.message_callback_add("camera/distance/V2", on_v2_distance)
#client.message_callback_add("command/V1", on_self_cmd)
client.message_callback_add("command/V2", on_v2_cmd)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

client.connect(broker_address, 1883,0) #connect to broker
client.loop_start() #start the loop

while not client.connected_flag:
    print("In Wait Loop")
    time.sleep(1)




#count = 0
try:
    #Loop indefinitely listening for calls to the publish function every 250ms
    while True:
        try:
            py_data = sio.loadmat('py_data.mat')
            send_msg(py_data)
            time.sleep(1) 
        #send_msg(3,py_data);
        #count += 1;
        except Exception:
            time.sleep(0.01)    

except KeyboardInterrupt:
    client.loop_stop()
    pass
