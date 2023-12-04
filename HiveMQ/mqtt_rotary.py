# import libraries
import network
from time import sleep
from umqtt.simple import MQTTClient
from machine import Pin
from rotary_irq_rp2 import RotaryIRQ

# log into WiFi network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID", "PASSWORD")
sleep(5)
print(wlan.isconnected())

# Define SW pin
SW=Pin(20,Pin.IN,Pin.PULL_UP)  

# Define RotaryIRQ
r = RotaryIRQ(pin_num_clk=18, pin_num_dt=19, min_val=0, reverse=False, range_mode=RotaryIRQ.RANGE_UNBOUNDED)  

# Define value
val_old = r.value()

# Define server, topic
mqtt_server = 'broker.hivemq.com'
client_id = 'bigles'
topic_pub = b'Me'

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

# Print values when Encoder is moved
while True:
    val_new = r.value()
    if SW.value()==0:
        print("Button Pressed")
        print("Selected Number is : ",val_new)
        print(b'selected number is {}'.format(val_new))
        client.publish(topic_pub, b'selected number is {}'.format(val_new))
    while SW.value()==0:
        continue
    if val_old != val_new:
        val_old = val_new
        print('result =', val_new)
    sleep(2)
