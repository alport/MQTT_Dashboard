# MQTT_Dashboard
 A dashboard which is updated via MQTT payloads from aMesh, a simple LoRa ESP32 based network, using the LoRa protocol that is currently in development.

 An aMesh gateway sends messages via a serial link to a Raspberry Pi computer running Node-Red. These Node-Red payloads are sent to a cloud-based Shiftr broker.

 In order to have universal access to the payload traffic, the MQTTdashboard subscribes to these messages using the PahoMqtt python library.

 The problem is that the incoming messsages are processed by a "on-receive" callback. If a StreamLit command such a st.table is included in this callback, StreamLit objects (with an out of context error), and hence, as a compromise, this st.table command needs to be executed in a sleep loop. Need to find a better solution.
