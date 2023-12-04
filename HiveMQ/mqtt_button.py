# import libraries
import network
from time import sleep
from picozero import Button
from umqtt.simple import MQTTClient
import machine

# log into WiFi network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("TC8717TDA", "TC8717T9344DA")
sleep(5)
print(wlan.isconnected())

# Define button
button = Button(16)

# Define server, topic and message
mqtt_server = 'broker.hivemq.com'
client_id = 'bigles'
topic_pub = b'Me'
topic_msg = b'door opened'

# Connect to server
def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

# Reconnect if failed
def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    sleep(5)
    machine.reset()

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

#If button pressed publish message
while True:
    if button.is_pressed:
        client.publish(topic_pub, topic_msg)
        sleep(2)
    else:
        pass
