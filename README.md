# MQTT_Dashboard
 A dashboard which is updated via MQTT payloads from aMesh.

 An aMesh gateway sends messages via a serial link to a Raspberry Pi computer running Node-Red. These Node-Red payloads are sent to a cloud-based Shiftr broker.

 In order to have universal access to the payload traffic, the MQTTdashboard subscribes to these messages using the PahoMqtt python library.

 The problem is that the incoming messsages are processed by a "on-receive" callback. If a StreamLit command such a st.table is included in this callback, StreamLit objects, and hence, this st.table command needs to be executed in a slleep loop.
