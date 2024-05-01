# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
#
# MJPEG Streaming
#
# This example shows off how to do MJPEG streaming to a FIREFOX webrowser
# Chrome, Firefox and MJpegViewer App on Android have been tested.
# Connect to the IP address/port printed out from ifconfig to view the stream.

import sensor
import time
import network
import socket
import utime
import pyb
import random
import sensor, image, os, tf, math, uos, gc

from machine import LED



# interupts


# interrupts end.


SSID = "Case"  # Network SSID
KEY = "pass123@"  # Network key
HOST = ""  # Use first available interface
PORT = 8080  # Arbitrary non-privileged port

# Init sensor


sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time=2000)          # Let the camera adjust.
buzzer_pin = pyb.Pin('A0', pyb.Pin.OUT_PP)

led_green = LED("LED_GREEN")
led_red = LED("LED_RED")
led_blue = LED("LED_BLUE")



def buzzer_on():
    buzzer_pin.value(True)

def buzzer_off():
    buzzer_pin.value(False)

flag=False
flag_led = False
color = 0
def buzzer_toggle(timer):
    global flag

    buzzer_pin.value(flag)
    flag=False

#def led_toggle():
#    global flag_led
#    global color

#    if(color==0):
#        led_off(0)
#        return
#    if(flag_led==False):
#        flag_led=True
#        led_off(0)
#    else:
#        flag_led= False
#        led_on(color)




def led_on(color):
    if(color == 0):
        led_off()

    elif(color==1):
        ledon_red()
    elif(color==2):
        ledon_green()
    elif(color==3):
        ledon_blue()
    elif(color==4):
        ledon_yellow()
    elif(color==5):
        ledon_magenta()
    elif(color==6):
        led_onwhite()


def led_off():
    led_red.off()
    led_green.off()
    led_blue.off()

def ledon_yellow():
    led_red.on()
    led_green.on()

def ledon_red():
    led_red.on()

def ledon_blue():
    led_blue.on()


def ledon_green():
    led_green.on()

def ledon_white():
    led_red.on()
    led_green.on()
    led_blue.on()


def ledon_magenta():
    led_red.on()
    led_blue.on()







timer = pyb.Timer(4, freq=10)
timer.callback(buzzer_toggle)

#timer2 = pyb.Timer(2, freq=10)
#timer2.callback(led_toggle)


net = None
labels = None
min_confidence = 0.5

# Init wlan module and connect to network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, KEY)

while not wlan.isconnected():
    print('Trying to connect to "{:s}"...'.format(SSID))
    time.sleep_ms(1000)

# We should have a valid IP now via DHCP
print("WiFi Connected ", wlan.ifconfig())

ledon_blue()
time.sleep_ms(500)
led_off()
time.sleep_ms(500)

# Create server socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

# Bind and listen
s.bind([HOST, PORT])
s.listen(5)

# Set server socket to blocking
s.setblocking(True)


def start_streaming(s):



    try:
        # load the model, alloc the model file on the heap if we have at least 64K free after loading
        net = tf.load("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
        print("Model Loaded.")
    except Exception as e:
        raise Exception('Failed to load "trained.tflite", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

    try:
        labels = [line.rstrip('\n') for line in open("labels.txt")]
    except Exception as e:
        raise Exception('Failed to load "labels.txt", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

    colors = [ # Add more colors if you are detecting more than 7 types of classes at once.
        (255,   0,   0),
        (  0, 255,   0),
        (255, 255,   0),
        (  0,   0, 255),
        (255,   0, 255),
        (  0, 255, 255),
        (255, 255, 255),
    ]


    print("Waiting for connections..")
    client, addr = s.accept()
    # set client socket timeout to 5s
    client.settimeout(5.0)
    print("Connected to " + addr[0] + ":" + str(addr[1]))

    ledon_yellow()
    time.sleep_ms(500)
    led_off()
    time.sleep_ms(500)

    # Read request from client
    data = client.recv(1024)
    # Should parse client request here

    # Send multipart header
    client.sendall(
        "HTTP/1.1 200 OK\r\n"
        "Server: OpenMV\r\n"
        "Content-Type: multipart/x-mixed-replace;boundary=openmv\r\n"
        "Cache-Control: no-cache\r\n"
        "Pragma: no-cache\r\n\r\n"
    )

    # FPS clock
    clock = time.clock()


    # Start streaming images
    # NOTE: Disable IDE preview to increase streaming FPS.

    while True:
        global flag
        global flag_led
        global color


        clock.tick()  # Track elapsed milliseconds between snapshots().




        img = sensor.snapshot()



        color = 0
        # detect() returns all objects found in the image (splitted out per class already)
        # we skip class index 0, as that is the background, and then draw circles of the center
        # of our objects
        led_off()

        for i, detection_list in enumerate(net.detect(img, thresholds=[(math.ceil(min_confidence * 255), 255)])):
            if (i == 0): continue # background class
            if (len(detection_list) == 0): continue # no detections for this class?

            print("********** %s **********" % labels[i])
            color=0

            #no color

            for d in detection_list:




                flag=True
                #print(i)


                if(i==2 or i==3 or i==4 or i==7 or i==8):
                    led_on(1)
                    #color red
                elif(i==1 or i==5):
                    led_on(2)
                    #color green
                elif(i==7):
                    led_on(9)
                    #color magenta
                elif(i==6):
                    led_on(3)
                else:
                    led_on(6)
                    #color white

                [x, y, w, h] = d.rect()
                center_x = math.floor(x + (w / 2))
                center_y = math.floor(y + (h / 2))
                print('x %d\ty %d' % (center_x, center_y))
                print("Detected sign : " , labels[i])

                #img.draw_circle((center_x, center_y, 12), color=colors[i], thickness=2)
                img.draw_rectangle(x,y,w,h)
                img.draw_string(x,y, labels[i], scale=1)

                #img.save("snapshot-%d.jpg" % random.getrandbits(32))




        cframe = img.compressed(quality=50)
        header = (
            "\r\n--openmv\r\n"
            "Content-Type: image/jpeg\r\n"
            "Content-Length:" + str(cframe.size()) + "\r\n\r\n"
        )
        client.sendall(header)
        client.sendall(cframe)







        #print(clock.fps(), "fps", end="\n\n")






while True:
    try:
        start_streaming(s)
    except OSError as e:
        print("socket error: ", e)
        # sys.print_exception(e)
