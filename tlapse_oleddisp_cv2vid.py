#!/usr/bin/env python

#using Adafruit_SSD1306_python library to display on a cheap I2C OLED display
# 3 buttons wired from 3.3v with a 1K current limiting resistor (probably should be more - might be - can't remember what value actually)

#import libraries needed - so opencv is needed - that is fun to install - use sudo apt-get install python.opencv - sorry if dependencies not mentioned here - might need scipy

import RPi.GPIO as gpio
import os, cv2, Adafruit_SSD1306
from picamera import PiCamera
from picamera.array import PiRGBArray
from datetime import datetime
from time import sleep
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# "WHAT YEAR IS IT?!!!"
now = datetime.now()
x = now.strftime("%Y")+"-"+now.strftime("%m")+"-"+now.strftime("%d")+"-"+now.strftime("%H")+"-"+now.strftime("%M")  #string of dateandtimestart
print(x)
# Define GPIO pins for buttons
in1 = 4 #button 1
in2 = 27 #button 2
in3 = 17 #button 3

#######################################################
def main():
  # Main program block
  #Initialise OLED display

  RST = None
  disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
  
  # Initialize library.
  disp.begin()

  # Clear display.
  disp.clear()
  disp.display()
  
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
  width = disp.width
  height = disp.height
  image = Image.new('1', (width, height))

# Get drawing object to draw on image.
  draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
  draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
  padding = 2
  top = padding

  # Load default font.
  font = ImageFont.truetype("//home/pi/Super Mario Bros. 2.ttf", 7)  #  you get two lines to play with

  #setup input pins
  gpio.setmode(gpio.BCM)       # Use BCM GPIO numbers
  gpio.setwarnings(False)
  gpio.setup(in1, gpio.IN, pull_up_down=gpio.PUD_DOWN)     # left button
  gpio.setup(in2, gpio.IN, pull_up_down=gpio.PUD_DOWN)     # middle button
  gpio.setup(in3, gpio.IN, pull_up_down=gpio.PUD_DOWN)     # right button

  left = 0
  period = 1
  while True: # choose the time between images
    topstring = "Time apart (s)"
    bottomstring = str(period)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((left, top), topstring,  font=font, fill=255)
    draw.text((left, top+16), bottomstring,  font=font, fill=255)
    disp.image(image)
    disp.display()
    if gpio.input(in1):
      sleep(0.05)
      if gpio.input(in1):
        period +=1
    elif gpio.input(in2):
      sleep(0.05)
      if gpio.input(in2):
        if period >= 2:
          period += -1
        else:
          period = 1
    if gpio.input(in3):
      sleep(0.2)
      if gpio.input(in3):
          break
  topstring = "Image total"
  bottomstring = ""
  draw.rectangle((0,0,width,height), outline=0, fill=0)
  draw.text((left, top), topstring,  font=font, fill=255)
  draw.text((left, top+16), bottomstring,  font=font, fill=255)
  disp.image(image)
  disp.display()
  sleep(0.5)
   
  imagenum = 100

  while True: # choose the number of images
    topstring = "Image total"
    bottomstring = str(imagenum)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((left, top), topstring,  font=font, fill=255)
    draw.text((left, top+16), bottomstring,  font=font, fill=255)
    disp.image(image)
    disp.display()
    if gpio.input(in1):
      sleep(0.05)
      if gpio.input(in1):
        imagenum += 100
    elif gpio.input(in2):
      sleep(0.1)
      if gpio.input(in2):
        sleep(0.1)
        if imagenum >= 200:
          imagenum += -100
        else:
          imagenum = 100
    if gpio.input(in3):
      sleep(0.2)
      if gpio.input(in3):
          break

  topstring = "Now Imaging"
  bottomstring = "See you later"
  draw.rectangle((0,0,width,height), outline=0, fill=0)
  draw.text((left, top), topstring,  font=font, fill=255)
  draw.text((left, top+16), bottomstring,  font=font, fill=255)
  disp.image(image)
  disp.display()

  os.chdir ("/home/pi/t_lapse")
  os.mkdir(x)
  os.chdir(x)
  filename = x + ".avi"
  camera = PiCamera()
  camera.resolution=(1920,1088)
  camera.vflip = True
  camera.hflip = True
  camera.color_effects = (128,128) #makes a black and white image for IR camera
  sleep(0.1)
  out = cv2.VideoWriter(filename, cv2.cv.CV_FOURCC(*'XVID'), 30, (1920,1088))
  for c in range(imagenum):
      with PiRGBArray(camera, size=(1920,1088)) as output:
          camera.capture(output, 'bgr')
          imagec = output.array
          out.write(imagec)
          output.truncate(0) #trying to get more than 300mb files..
          pass
      sleep(period-0.5)
      remaining = imagenum - (c-1)
      bottomstring = str(remaining)+" remain"
      draw.rectangle((0,0,width,height), outline=0, fill=0)
      draw.text((left,top), topstring, font=font, fill=255)
      draw.text((left,top+16), bottomstring, font=font, fill=255)
      disp.image(image)
      disp.display()
  camera.close()
  out.release()

  image = Image.new('1', (width, height))
  topstring = "Now Finished"
  bottomstring = "Let's look"
  draw.rectangle((0,0,width,height), outline=0, fill=0)
  draw.text((left, top), topstring,  font=font, fill=255)
  draw.text((left, top+16), bottomstring,  font=font, fill=255)
  disp.image(image)
  disp.display()
####################################################

if __name__ == '__main__':
  main()
