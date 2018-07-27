#!/bin/bash
#sysinfo_page - Autostart daemons for PiDrivR 
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock
sleep 5
sudo kismet_server -s --daemonize
sudo python /home/pi/PiDrivR/wardrive.py