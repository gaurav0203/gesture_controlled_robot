# boot.py -- run on boot-up
try:
  import usocket as socket
except:
  import socket

from machine import Pin, Signal
import network

import esp
esp.osdebug(None)

import gc
gc.collect()
# modify ssid(wifi name) and password
ssid = 'wifi_name'
password = 'wifi_password'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('\n\n\nConnection successful\n')
print(station.ifconfig())

left_forward_pin = Pin(4, Pin.OUT)
left_forward = Signal(left_forward_pin, invert=False)

left_reverse_pin = Pin(5, Pin.OUT)
left_reverse = Signal(left_reverse_pin, invert=False)

right_forward_pin = Pin(12, Pin.OUT)
right_forward = Signal(right_forward_pin, invert=False)

right_reverse_pin = Pin(13, Pin.OUT)
right_reverse = Signal(right_reverse_pin, invert=False)

