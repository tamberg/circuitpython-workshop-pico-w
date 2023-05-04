import ssl
import time
import wifi
import socketpool

import adafruit_requests

WIFI_SSID = "MY_SSID" # TODO
WIFI_PASS = "MY_PASSWORD" # TODO
CLOUD_KEY = "****************" # TODO, ThingSpeak Write API Key
CLOUD_URL = "https://api.thingspeak.com/update.json"

print("Connecting to Wi-Fi \"{0}\"...".format(WIFI_SSID))
wifi.radio.connect(WIFI_SSID, WIFI_PASS) # waits for IP address
print("Connected, IP address = {0}".format(wifi.radio.ipv4_address))

socket = socketpool.SocketPool(wifi.radio)
context = ssl.create_default_context()
https = adafruit_requests.Session(socket, context)

while True:
    value = 23.0 # e.g. from sensor
    json_data = {
        "api_key": CLOUD_KEY,
        "field1": value, 
    }
    print("Posting to {0}\n> {1}".format(CLOUD_URL, json_data))
    response = https.post(CLOUD_URL, json=json_data)
    print("< {0}".format(response.json()))
    time.sleep(30) # s
