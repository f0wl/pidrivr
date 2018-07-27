#!/usr/bin/env python

import os
import sys
import time
import subprocess
import gps
import RPi.GPIO as GPIO
sys.path.append("/home/pi/PiDrivR/kismetclient/kismetclient")
from papirus import Papirus
from PIL import Image
from papirus import PapirusComposite
from kismetclient import Client
from kismetclient import handlers

papirus = Papirus()

SW1 = 16
SW2 = 26
SW3 = 20
SW4 = 21

GPIO.setmode(GPIO.BCM)

GPIO.setup(SW1, GPIO.IN)
GPIO.setup(SW2, GPIO.IN)
GPIO.setup(SW3, GPIO.IN)
GPIO.setup(SW4, GPIO.IN)

kismet_stat = gpsd_stat = 0
total = wpa = wep = none = wps = 0
aps = []
k = Client()

# Check EPD_SIZE is defined
EPD_SIZE=0.0
if os.path.exists('/etc/default/epd-fuse'):
    exec(open('/etc/default/epd-fuse').read())
if EPD_SIZE == 0.0:
    print("Please select your screen size by running 'papirus-config'.")
    sys.exit()

def count_crypts(client, name, macaddr, cryptstring):
    global aps, total, wpa, wep, none, wps
    pairing = (name, macaddr)
    if pairing not in aps:
        aps.append(pairing)
        if 'None' in cryptstring:
            none += 1
        elif 'WPA' in cryptstring:
            wpa += 1
        elif 'WEP' in cryptstring:
            wep += 1
        elif 'WPS' in cryptstring:
            wpa += 1
            wps += 1
        elif cryptstring == '':
            none += 1
        total = len(aps)

address = ('127.0.0.1', 2501)
k = Client(address)
k.register_handler('TRACKINFO', count_crypts)

def runKismet():
  kismet = subprocess.Popen(['ps -ef | grep kismet'],
  stdout=subprocess.PIPE, shell=True)
  (output, error) = kismet.communicate()
  if 'kismet_server' in output:
        kismet_stat = "1"
  else:
        print("Kismet Daemon not running!")

def runGPSD():
  gps = subprocess.Popen(['ps -ef | grep gpsd'],
  stdout=subprocess.PIPE, shell=True)
  (output, error) = gps.communicate()
  if 'gpsd' in output:
      gpsd_stat = "1"
  else:
      print("GPSD Daemon not running!")

def update_aps(wpa, wep, wps, none, total):
  text = PapirusTextPos(False)
  text.AddText("Total APs:", 67, 30)
  text.AddText(total, 80, 30, Id="c_total" )
  text.AddText("WPA......:", 67, 40)
  text.AddText(wpa, 80, 40, Id="c_wpa" )
  text.AddText("WEP......:", 67, 50)     
  text.AddText(wep, 80, 50, Id="c_wep" )
  text.AddText("WPS......:", 67, 60)
  text.AddText(wps, 80, 60, Id="c_wps" )
  text.AddText("None.....:", 67, 70)
  text.AddText(none, 80, 70,  Id="c_none" )
  text.UpdateText("c_total",total)
  text.UpdateText("c_wpa", wpa)
  text.UpdateText("c_wep", wep)
  text.UpdateText("c_wps", wps)
  text.UpdateText("c_none", none)

def main():
    print("Writing to Papirus.......")
    textNImg = PapirusComposite(False)
    textNImg.AddText('PiDrivR', 83, 20, 20)
    textNImg.AddText('WELCOME!', 92, 50, 15)
    textNImg.AddText('https://pidrivr.f0wl.cc', 54, 80, 10)
    image = 'logo.jpg'
    textNImg.AddImg(image , 0, 0, (55, 95))
    textNImg.WriteAll()
    print("Finished Splashscreen!")
    time.sleep(10)
    papirus.clear()
    textNImg = PapirusComposite(False)
    textNImg.AddText('PiDrivR', 83, 5, 15)
    textNImg.AddText('https://pidrive.f0wl.cc', 55, 80, 10)
    image = 'logo.jpg'
    textNImg.AddImg(image , 0, 0, (55, 95))
    while True:
       k.listen()
       runKismet()
       runGPSD()
       update_aps(wpa, wep, wps, none, total)
    if kismet_stat == 1:
       image2 = 'kismet.jpg'
       textNImg.AddImg(image2 , 100, 2, (10, 12))
    if gpsd_stat == 1:
       image3 = 'gps.jpg'
       textNImg.AddImg(image3, 115, 2, (12, 12))
    textNImg.WriteAll()
    papirus.update()

if __name__ == '__main__':
    main()
