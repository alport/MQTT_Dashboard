# Good tutorial:
# http://www.steves-internet-guide.com/mqtt-python-beginners-course/
# http://www.steves-internet-guide.com/python-mqtt-publish-subscribe/
# need to check all numbers in payload are not NaN np.isnan(np.nan)
import time
import paho.mqtt.client as paho
import numpy as np
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

broker="solarcrest962.cloud.shiftr.io"

#slots=np.array([1,2,6,9],dtype=np.int32) # Dunkirk
slots=np.array([0,3,4,7],dtype=np.int32) # Highlands
#nodes=[0,1,2,3,4,5,6,7,8,9] # not used??

table=np.zeros((10,len(slots)*3),dtype=np.int32)
Ttable=np.zeros(len(slots),dtype=np.int32)
ncolumns=table.shape[1]

tableData = st.empty()
TtableData=st.empty()

def checkPayload(parts,nvals):
    state=True
    if (len(parts)!=nvals):
        state=False
        return state
    for i in range(len(parts)):
        if(parts[i]=='NaN'):
            state=False
            return state
    return state

# processT
def processT(payload):
    global Ttable
    Tparts=payload.split(",")
    if checkPayload(Tparts,2):
        Tarray = np.array(Tparts,dtype=np.int32)
        nslot=Tarray[0]
        for i in range(len(slots)):   
            if (nslot==slots[i]):
                ncol= np.where(slots == nslot)[0][0]
                Ttable[ncol]=Tarray[1]
    else:
        print("Error, NaN in: ",Tparts)

def processD(payload):
    global table
    Dparts=payload.split(",")
    if checkPayload(Dparts,7):  # Dumkirk:5, Highlands:7
        Darray = np.array(Dparts,dtype=np.int32)
        for i in range(len(slots)):
            nslot=Darray[4]  # was 0!!! error?
            if (nslot==slots[i]):
                ncol = np.where(slots == nslot)[0][0]*3
                nnode=Darray[0]
                table[nnode,ncol:ncol+3]=Darray[1:4]
    else:
        print("Error, NaN in: ",Dparts)

def on_message(client, userdata, msg):
    time.sleep(1)
    topicT="Highlands/data/T"
    topicD="Highlands/data/D"
    print("Received",msg.topic,",",str(msg.payload.decode("utf-8")))
    payload=str(msg.payload.decode("utf-8"))
    if (msg.topic==topicT):
        #print("processT")
        processT(payload)
    if (msg.topic==topicD):
        #print("processD")
        processD(payload)
    #df = pd.DataFrame(table,columns=('col %d' % i for i in range(ncolumns)))
    #st.table(df)    
    
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    topic="Highlands/data/#"
    print("Subscribing to: "+topic)
    #client.subscribe("Dunkirk/data/#")
    client.subscribe("Highlands/data/#")
    

client= paho.Client("client-001") #create client object 
#client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) 
#establish connection client1.publish("house/bulb1","on")
######Bind function to callback
client.on_message=on_message
client.on_connect = on_connect
#####

print("connecting to broker ",broker)
client.username_pw_set(username="solarcrest962",password="28zvKkReyN3VhW8W")
client.connect(broker, 1883, 60)

client.loop_start() #start loop to process received messages  - BETTER can ctrl C!!!
#client.loop_forever()
while True:
    tableData.write(table)
    #TtableData.write(Ttable)
    TtableData.write(pd.DataFrame({
        'Slot '+str(slots[0]):[Ttable[0]],
        'Slot '+str(slots[1]):[Ttable[1]],
        'Slot '+str(slots[2]):[Ttable[2]],
        'Slot '+str(slots[3]):[Ttable[3]]
        }))
    #print("Updating:",i)
    time.sleep(2)
