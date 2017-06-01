
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import serial
import string


class OpenMV(object):

        def __init__(self):
                self.ser = serial.Serial(port='/dev/ttyAMA0',baudrate=9600, timeout = 0.2)
                # Raspberry Pi pin configuration:
                RST = 24
                # Note the following are only used with SPI:
                DC = 23
                SPI_PORT = 0
                SPI_DEVICE = 0
                # 128x32 display with hardware I2C:
                #self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
                # 128x64 display with hardware I2C:
                self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
                # Initialize library.
                self.disp.begin()

                # Clear display.
                self.disp.clear()
                self.disp.display()

                # Create blank image for drawing.
                # Make sure to create image with mode '1' for 1-bit color.
                width = self.disp.width
                height = self.disp.height
                self.image = Image.new('1', (width, height))

                # Get drawing object to draw on image.
                self.draw = ImageDraw.Draw(self.image)
                padding = 2
                shape_width = 20
                top = padding
                bottom = height-padding
                x = padding
                x += shape_width+padding

                # Load default font.
                #self.font = ImageFont.load_default()
                self.font = ImageFont.truetype('Minecraftia-Regular.ttf', 8)


        def balloon_xysize(self):
            balloon_found = False
            balloon_x = 0
            balloon_y = 0
            balloon_radius = 0
            w = 0
            
            line = self.ser.readline()
            words = string.split(line , ";")    # Fields split
            if len(words) > 3:
                    self.disp.clear()
                    self.disp.display()
                    balloon_x = int (words [0])
                    balloon_y = int (words [1])
                    w = int (words [2])
                    h = int (words [3])
                    balloon_radius = w 
                    #clock = float (words [4]) 
                    balloon_found = True
            
            else:
                balloon_found = False
                balloon_x = 0
                balloon_y = 0
                balloon_radius = 0
                w = 0
                #print "Invalid line"


            print balloon_found, balloon_x, balloon_y, balloon_radius    
            self.draw.text((12, 2), (" %d " % (balloon_found)) , font=self.font, fill=255)
            self.draw.text((12, 12), (" %d " % (balloon_x)) , font=self.font, fill=255)
            self.draw.text((12, 22), (" %d " % (balloon_y)) , font=self.font, fill=255)
            self.draw.text((12, 32), (" %d " % (balloon_radius)) , font=self.font, fill=255)
            self.disp.image(self.image)
            self.disp.display()
            self.ser.close
            #print "closed"
            return balloon_found, balloon_x, balloon_y, balloon_radius

        
              
        # main - tests the Openmv class
        def main(self):
                while True:
                    self.balloon_xysize()


   
# create the global balloon_finder object
open_mv = OpenMV()

# run a test if this file is being invoked directly from the command line
if __name__ == "__main__":
    open_mv.main()
