# import libraries
import network
from time import sleep
from picozero import Button
from umqtt.simple import MQTTClient
import machine

# Log into WiFi Network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID", "PASSWORD")
sleep(5)
print(wlan.isconnected())

# Define buttons
button = Button(16)
button2 = Button(15)

# Define server, topic and messages
mqtt_server = 'broker.hivemq.com'
client_id = 'bigles'
topic_pub = b'Me'
topic_msg = b'door opened'
topic_msg2 = b'door closed'

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

# When either button is pressed publish to topic
while True:
    if button.is_pressed:
        client.publish(topic_pub, topic_msg)
        sleep(2)
    elif button2.is_pressed:
        client.publish(topic_pub, topic_msg2)
        sleep(2)
    else:
        pass
