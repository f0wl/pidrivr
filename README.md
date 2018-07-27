# PiDrivR ![status](https://pidrivr.f0wl.cc/img/status.svg)
:car: :satellite: A wardriving companion featuring the RaspberryPi 3B+ and PaPiRus e-paper Display
![Image of PiDrivR](https://pidrivr.f0wl.cc/img/pidrivr-small.png)

Hey, thanks for checking out PiDrivR, yet another wardriving script for the RaspberryPi. As you can see in the image above it is tailored to run with the PiSupply "PaPiRus" e-Paper Screen (for me it is the 2.0" Version). If you like the Idea of wardriving with the Raspi, but you don't want to spend your money on the e-Paper Display here are some alternatives that use a different or no screen:

* Piwardrive (LEDs, Wigle support) [GitHub](https://github.com/Wardriving-for-Raspberry-PI-v-B/Piwardrive)
* KismetPiDisplay (Adafruit LCD) [GitHub](https://github.com/ThaWeatherman/KismetPiDisplay)

Scott Helme also created a very good writeup on wardriving with the Pi: [scotthelme.co.uk](https://scotthelme.co.uk/wifi-wardriving/)

## Hardware
As a reference here are the parts that I used for my wardriving build, but as long as your wireless card has driver and kismet support and the gps dongle works with gpsd you can choose freely.

* RaspberryPi Model 3 B+ 
* PiSupply PaPiRus e-Paper HAT 2.0"
* GlobalSat Navigation Antenna BU-353
* Alfa AWUS051NH V2
* Samsung 64GB Evo MicroSD

## Installation
For a quick and easy Install I wrote a small bash script that gets PiDrivR up and running in next to no time. You'll only have to run this command:
```
curl -sSL https://pidrivr.f0wl.cc/install.sh | sudo bash
```
### A quick overview of what the script will be doing:
1. Make sure your Raspbian OS is up to date
2. Clone this repository
3. Install all software dependencies (including Kismet)
4. Install the PaPiRus Software for the e-Paper Display
5. Download Patrick Salecker's .netxml to .kml script

Please remember to enable SPI and I²C via ```sudo rasp-config```, otherwise the e-Paper display will not work.

Next: Run ```sudo nano /etc/default/gspd``` to edit the configuration file of the gps daemon and make sure the following values are set:
```
START_DAEMON="true"
GPSD_OPTIONS="-n"
DEVICES="/dev/ttyUSB0" 
USBAUTO="true"
GPSD_SOCKET="/var/run/gpsd.sock"
```
To successfully run kismet we have to edit its configuration file as well by typing ```sudo nano /usr/local/etc/kismet.conf```. Press Ctrl+W on your Keyboard and type ```ncsource=```. For Raspberry Pis with integrated Wireless-LAN capabilities ```wlan0``` has to be changed to ```wlan1```. After that, press Ctrl+W again and search for ```logtypes=```. We only need ```netxml,gpsxml``` and you can delete the remaining logtypes.
