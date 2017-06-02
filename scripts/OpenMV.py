
import serial
import string


class OpenMV(object):

        def __init__(self):
            self.ser = serial.Serial(port='/dev/ttyAMA0',baudrate=115200, timeout = 0.5)
            self.ser.flushInput();
   
        def balloon_xysize(self):
            balloon_found = False
            balloon_x = 0
            balloon_y = 0
            balloon_radius = 0
            w = 0
            
            self.ser.flushInput();
            line = self.ser.readline()
            words = string.split(line , ";")    # Fields split
            if len(words) > 3:
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
            
            #print "closed"
            #return balloon_found, balloon_x, balloon_y, balloon_radius
        

        
              
        # main - tests the Openmv class
        def main(self):
                while True:
                    self.balloon_xysize()
                      
                exit(1)
                self.ser.close
   
# create the global balloon_finder object
open_mv = OpenMV()

# run a test if this file is being invoked directly from the command line
if __name__ == "__main__":
    open_mv.main()
