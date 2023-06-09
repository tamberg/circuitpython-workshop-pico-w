# IoT Embedded Programming with CircuitPython

> TODO: Port examples and images to Raspberry Pi Pico W

## Workshop
The Internet of Things ([IoT](http://www.tamberg.org/fhnw/2021/hs/IoT01Introduction.pdf)) is the convergence of internet and real world. IoT embedded devices typically have limited resources, but they are also becoming more performant with each generation. This allows an interpreted language like Python, which is less efficient but more convenient than C, to run on a microcontroller.

### Topics
- [Introduction](#introduction)
- [Toolchain Setup](#toolchain-setup)
- [Hardware Setup](#hardware-setup)
- [GPIO & Sensors](#gpio--sensors)
- [Wi-Fi, HTTP & MQTT](#wifi--http--mqtt)

### Objective
This workshop teaches the basics of embedded programming on the latest IoT hardware, with CircuitPython.

### Target audience
This workshop is aimed at interested people with basic programming experience in Python.

### Prerequisites
Participants need a laptop with MacOS, Windows or Linux, and one USB/USB-C port. IoT hardware including sensors is available on loan.

The workshop requires a Wi-Fi network that is accessible without a portal. Alternatively, a personal smartphone can be used as a hotspot.

## Introduction
### CircuitPython
> The easiest way to program microcontrollers — https://circuitpython.org/

To program a CircuitPython microcontroller, plug it in via USB.

It shows up as a USB drive called _CIRCUITPY_.

(If not, see [hardware setup](#hardware-setup).)

## Toolchain setup
### Code editor
CircuitPython works with any text editor, e.g. [Mu Editor](https://codewith.mu/), [VS Code](https://code.visualstudio.com/), or *nano*.

```
$ nano /Volumes/CIRCUITPY/code.py
```

### Serial monitor
To see output you'll need a serial monitor like [PuTTY](https://www.putty.org/) on Windows or *screen* on MacOS, Linux (or [tio](https://github.com/tio/tio#4-installation)).

```
$ screen /dev/tty.u<TAB> 115200
```

If there is no output, use CTRL-D to reload

```
Hello, World!

Code done running.
```

Or press any other key to enter the REPL
```
>>>
```

### CircuitPython libraries
Download the library bundle ZIP file from https://circuitpython.org/libraries

You will selectively copy files from the ZIP to your microcontroller later on.

### Run Python code
Plug in your board via USB and open the _CIRCUITPY_ drive.

Copy required libraries from the bundle to the _lib_ folder.

Copy your code to a file named _code.py_ on the drive.

```
$ cp hello/code.py /Volumes/CIRCUITPY/code.py
```

Now you are ready to try [GPIO & sensors](#gpio--sensors).

## Hardware setup
We use a [Pico W microcontroller](#pico-w) with [Grove sensors and actuators](#grove-sensors--actuators).

### Pico W
#### Buy
* https://www.adafruit.com/product/5526 (Raspberry Pi Pico W)
* https://www.adafruit.com/product/3879 (USB C to USB Micro cable for data transfer)
* https://www.adafruit.com/product/4175 (USB A to USB C adapter, optional)

#### Board
https://circuitpython.org/board/raspberry_pi_pico_w/

#### Pico W ROM bootloader mode (once)
To get the Pico W into ROM bootloader mode

* Press and hold the _BOOTSEL_ button
* Unplug, then plug in the Pico W via USB

Now the board should show up as a USB device, e.g. /dev/cu.usbmodem01 on MacOS or COM3 on Windows.

#### Install CircuitPython (once)
Download the board specific .UF2 file from https://circuitpython.org/board/raspberry_pi_pico_w/

Drop it on the USB drive named _RPI-RP2_ and wait until the drive disconnects.

Now the board should show up as a USB drive named _CIRCUITPY_.

#### Troubleshooting
* https://learn.adafruit.com/pico-w-wifi-with-circuitpython/installing-circuitpython#flash-resetting-uf2-3128829 (Flash resetting UF2)
* https://learn.adafruit.com/welcome-to-circuitpython/troubleshooting

#### Pinout
<img text="Pico W Pinout, (c) Raspberry Pi" src="https://www.raspberrypi.com/documentation/microcontrollers/images/picow-pinout.svg" width="800"/>

* https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html#pinout-and-design-files-2 (Pinout)

#### Schematic
<img text="Pico W Schematic, (c) Raspberry Pi" src="TODO" width="640"/>

* TODO (Schematic)

#### Datasheets
* [Pico W Datasheet](https://datasheets.raspberrypi.com/picow/pico-w-datasheet.pdf)
* [RP2040 Datasheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf)

### Grove sensors & actuators
#### Buy
* https://www.seeedstudio.com/Grove-Button-p-766.html
* https://www.seeedstudio.com/Grove-Red-LED-p-1142.html
* https://www.seeedstudio.com/Grove-Rotary-Angle-Sensor-p-770.html
* https://www.seeedstudio.com/Grove-Temperature-Humidity-Sensor-DHT1-p-745.html
* https://www.seeedstudio.com/Grove-4-pin-Male-Jumper-to-Grove-4-pin-Conversion-Cable-5-PCs-per-Pack.html

## GPIO & sensors
### Blink (digital output)
Control a LED or any other digital actuator.

<img src="QtPyEsp32S2BlinkWiring.png" width="320"/>

```
/CIRCUITPY
└── code.py # copied from below
```

```
import board
import digitalio
import time

actuator = digitalio.DigitalInOut(board.LED) # or board.GP1 (Grove), GP3 (Grove), GP8 (badge LED)
actuator.direction = digitalio.Direction.OUTPUT

while True:
    actuator.value = True
    time.sleep(1)
    actuator.value = False
    time.sleep(1)
```

```
# No output, but LED should blink
```

### Button (digital input)
Read a button or any other digital sensor.

<img src="QtPyEsp32S2ButtonWiring.png" width="320"/>

```
/CIRCUITPY
└── code.py # copied from below
```

```
import board
import digitalio
import time

sensor = digitalio.DigitalInOut(board.GP6) # or board.GP1 (Grove), GP3 (Grove)
sensor.direction = digitalio.Direction.INPUT
sensor.pull = digitalio.Pull.UP

while True:
    print(sensor.value)
    time.sleep(0.1)
```

```
False
False
True
...
```

### DHT11 temperature & humidity
Read a DHT11 sensor using the *adafruit_dht* [library](#circuitpython-libraries).

<img src="QtPyEsp32S2DhtWiring.png" width="400"/>

```
/CIRCUITPY
├── code.py # copied from below
└── lib # libraries from bundle
    └── adafruit_dht.mpy
```

```
import adafruit_dht
import board
import time

sensor = adafruit_dht.DHT11(board.D18)

while True:
    try:
        temp = sensor.temperature
        humi = sensor.humidity
        print("{:.2f} °C, {:.2f} %".format(temp, humi))

    except RuntimeError as e:
        print("Oops, reading the sensor did not work.")

    time.sleep(5)
```

```
23.00 °C, 42.00 %
...
```

### More
Search the [library bundle docs](https://docs.circuitpython.org/projects/bundle/en/latest/drivers.html) for a sensor or actuator name.

## Wi-Fi, HTTP & MQTT
### Wi-Fi connect
Connect to the Internet using Wi-Fi.

```
/CIRCUITPY
└── code.py # copied from below
```

```
import wifi

WIFI_SSID = "MY_SSID" # TODO
WIFI_PASS = "MY_PASSWORD" # TODO

print("Connecting to Wi-Fi \"{0}\"...".format(WIFI_SSID))
wifi.radio.connect(WIFI_SSID, WIFI_PASS) # waits for IP address
print("Connected, IP address = {0}".format(wifi.radio.ipv4_address))
```

```
Connecting to Wi-Fi "MY_SSID"...
Connected, IP address = 192.168.0.23

Code done running.
```
Once a device is connected to the Internet, it can send data to a cloud backend.

To see how this works, try the [HTTP post](#http-post) or [MQTT publish](#mqtt-publish) examples.

### HTTP post
Post data to the https://thingspeak.com/ cloud backend using HTTPS.

Create a free ThingSpeak account to get a Write API Key.

```
/CIRCUITPY
├── code.py # copied from below
└── lib # libraries from bundle
    └── adafruit_requests.mpy
```

```
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

```

```
Connecting to Wi-Fi "MY_SSID"...
Connected, IP address = 192.168.0.42
Posting to https://api.thingspeak.com/update.json
> {'field1': 23.0, 'api_key': '****************'}
< {'field1': 23.0, 'channel_id': 555, 'created_at': '2022-08-30T13:37:00Z', ...
```
Now, try to merge in the [DHT11 example](#dht11-temperature--humidity) to send real sensor values.

Or learn more about [Internet protocols and HTTP](http://www.tamberg.org/fhnw/2021/hs/IoT04InternetProtocols.pdf).

### MQTT publish
Publish data to the https://thingspeak.com/ cloud backend using MQTT. 

```
/CIRCUITPY
├── code.py # copied from below
└── lib # libraries from bundle
    └── adafruit_minimqtt
        ├── __init__.py
        ├── adafruit_minimqtt.mpy
        └── matcher.mpy
```

```
from random import randint
import ssl
import time
import wifi
import socketpool
import adafruit_minimqtt.adafruit_minimqtt as minimqtt

WIFI_SSID = "MY_SSID" # TODO
WIFI_PASS = "MY_PASSWORD" # TODO

# See https://ch.mathworks.com/help/thingspeak/mqtt-basics.html
MQTT_HOST = "mqtt3.thingspeak.com"
MQTT_PORT = 8883

# https://thingspeak.com/devices/mqtt > Add a device
MQTT_CLNT = "***********************" # TODO, Client ID
MQTT_USER = "***********************" # TODO, Username
MQTT_PASS = "***********************" # TODO, Password
THSP_CHAN = "000000" # TODO, ThingSpeak Channel ID

print("Connecting to Wi-Fi \"{0}\"...".format(WIFI_SSID))
wifi.radio.connect(WIFI_SSID, WIFI_PASS) # waits for IP address
print("Connected, IP address = {0}".format(wifi.radio.ipv4_address))

pool = socketpool.SocketPool(wifi.radio)
context = ssl.create_default_context()

def handle_connect(client, userdata, flags, rc):
    print("Connected to {0}".format(client.broker))

def handle_publish(client, userdata, topic, pid):
    print("Published to {0} with PID {1}".format(topic, pid))

mqtt_client = minimqtt.MQTT(
    broker = MQTT_HOST,
    port = MQTT_PORT,
    client_id = MQTT_CLNT,
    username = MQTT_USER,
    password = MQTT_PASS,
    socket_pool = pool,
    ssl_context = context)

mqtt_client.on_connect = handle_connect
mqtt_client.on_publish = handle_publish

print("\nConnecting to {0}...".format(MQTT_HOST))
mqtt_client.connect()

while True:
    value = 23 # e.g. from sensor
    mqtt_topic = "channels/" + THSP_CHAN + "/publish"
    mqtt_payload = "field1=" + str(value)
    mqtt_client.publish(mqtt_topic, mqtt_payload)
    time.sleep(5)
```

Learn more about the [MQTT messaging protocol](http://www.tamberg.org/fhnw/2021/fs/IdbMessagingProtocols.pdf).
