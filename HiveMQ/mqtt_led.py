# import libraries
import network
from time import sleep
from picozero import LED
from umqtt.simple import MQTTClient
import machine

# Log into WiFi Network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID", "PASSWORD")
sleep(5)
print(wlan.isconnected())

# Define LED
led = LED(1)

# Define the MQTT server and topic
mqtt_server = 'broker.hivemq.com'
client_id = 'bigles'
topic_sub = b'Me'

# Define function that turns on or off the LED
def sub_cb(topic, msg):
    print("New message on topic {}".format(topic.decode('utf-8')))
    msg = msg.decode('utf-8')
    print(msg)
    if msg == "on":
        led.on()
    elif msg == "off":
        led.off()
      
# Define function that connects to server
def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=60)
    client.set_callback(sub_cb)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client
  
# Define function that reconnects
def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    sleep(5)
    machine.reset()

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
while True:
    client.subscribe(topic_sub)
    sleep(1)

