
import serial
import string

class OpenMV(object):

        def __init__(self):
            self.ser = serial.Serial(port='/dev/ttyAMA0',baudrate=19200, timeout = 0.2)

        def balloon_xysize(self):
            balloon_found = False
            balloon_x = 0
            balloon_y = 0
            balloon_distance = 0
            
            line = self.ser.readline()
            #print (line)
            words = string.split(line , ";")    # Fields split
            if len(words) > 2:
                    balloon_distance = int (words [0]) 
                    balloon_x = int (words [1])
                    balloon_y = int (words [2])
                    balloon_found = True
            #else:
                #print "Invalid line"
                                        
            print balloon_found, balloon_x, balloon_y, balloon_distance
            self.ser.close
            #print "closed"
            #return balloon_found, balloon_x, balloon_y, balloon_distance
        
              
        # main - tests the Openmv class
        def main(self):
                while True:
                    self.balloon_xysize()


   
# create the global balloon_finder object
open_mv = OpenMV()

# run a test if this file is being invoked directly from the command line
if __name__ == "__main__":
    open_mv.main()
