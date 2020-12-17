# RPi-PiLapse
Acquisition and Video rendering of Time lapse photography with a Raspberry Pi and RPi-Camera

This is setup with a 128x63 OLED using Adafruit SSD1306 library
I use 3 push buttons as controls for the display and to set image numbers and period

Using OpenCV to encode video
Picamera to take pictures

I'm using this specific code on a IR sensitive camera with IR leds so it is a night camera - have also implemented this in a couple of other ways 

Feel free to shout at me for how bad this is..

It doesn't currently create files larger than 366Mb which is limiting how many images I can actually take. Not sure why so this is not a finished deal
