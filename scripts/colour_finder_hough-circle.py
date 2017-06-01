#
# colour_finder.py - helps find the min and max Hue, Saturation and Brightness (aka Value) of a desired object
#
#   Start from command line using 'python colour_finder.py', select a window and press ESC at any time to quit
#
#   4 windows will be displayed:
#       Colour Filters : display high and low colour filters for Hue, Saturation and Brightness (aka Value)
#       Original : displays the raw image from the camera
#       Mask : displays black and white mask where black parts will be removed, white parts will remain
#       Filtered Result: Original image with Mask applied.  Only desired object should be visible
#
#   How to use:
#       Start the program and hold the object in front of the camera (the object should not fill the entire screen)
#       Increase the min and decrease the Max Hue, Saturation and Brightness trackbars so that only the desired object is shown in the Filtered Result
#       Record the values so they can be input manually into the usb_cam_test.py script

import cv2
import imutils
import numpy as np
import balloon_config
from balloon_video import balloon_video

class ColourFinder:

    # constructor
    def __init__(self):
        # initialise colour filters to no filtering
        self.h_low = 0
        self.h_high = 255
        self.s_low = 0
        self.s_high = 255
        self.v_low = 0
        self.v_high = 255

        # initialise save trackbar setting
        self.save = 0

    # call back for trackbar movements
    def empty_callback(self,x):
        pass

    # call back for save trackbar that saves colour filters to config file
    def save_callback(self,x):
        if x == 10:
            balloon_config.config.set_integer('balloon','h-low',self.h_low)
            balloon_config.config.set_integer('balloon','h-high',self.h_high)
            balloon_config.config.set_integer('balloon','s-low',self.s_low)
            balloon_config.config.set_integer('balloon','s-high',self.s_high)
            balloon_config.config.set_integer('balloon','v-low',self.v_low)
            balloon_config.config.set_integer('balloon','v-high',self.v_high)
            balloon_config.config.save();
            print "Saved colour filters to config file!"
        return

    # run - main routine to help user find colour filters
    def run(self):

        # initialise video capture
        balloon_video.init_camera()

        # create trackbars for color change
        cv2.namedWindow('Colour Filters')
        cv2.createTrackbar('Hue min','Colour Filters',self.h_low,255,self.empty_callback)
        cv2.createTrackbar('Hue max','Colour Filters',self.h_high,255,self.empty_callback)
        cv2.createTrackbar('Sat min','Colour Filters',self.s_low,255,self.empty_callback)
        cv2.createTrackbar('Sat max','Colour Filters',self.s_high,255,self.empty_callback)
        cv2.createTrackbar('Bgt min','Colour Filters',self.v_low,255,self.empty_callback)
        cv2.createTrackbar('Bgt max','Colour Filters',self.v_high,255,self.empty_callback)
        cv2.createTrackbar('Save','Colour Filters',0,10,self.save_callback)

        while(True):
            # get a frame
            frame = balloon_video.capture_image()
            output = frame.copy()
            
            # Convert BGR to HSV
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
            # get latest trackbar positions
            self.h_low = cv2.getTrackbarPos('Hue min','Colour Filters')
            self.h_high = cv2.getTrackbarPos('Hue max','Colour Filters')
            self.s_low = cv2.getTrackbarPos('Sat min','Colour Filters')
            self.s_high = cv2.getTrackbarPos('Sat max','Colour Filters')
            self.v_low = cv2.getTrackbarPos('Bgt min','Colour Filters')
            self.v_high = cv2.getTrackbarPos('Bgt max','Colour Filters')
        
            # use trackbar positions to filter image
            colour_low = np.array([self.h_low,self.s_low,self.v_low])
            colour_high = np.array([self.h_high,self.s_high,self.v_high])
        
            # Threshold the HSV image
            mask = cv2.inRange(hsv_frame, colour_low, colour_high)

            #PAPOU_MOD Hough Circle        
            #gray = cv2.cvtColor(mask, cv2.COLOR_HSV2GRAY)
            blurred = cv2.GaussianBlur(mask, (3,3), 0)
            
            #circles = cv2.HoughCircles(blurred, cv2.cv.CV_HOUGH_GRADIENT, 1.9, 60)

            # ensure at least some circles were found
            #if circles is not None:
                # convert the (x, y) coordinates and radius of the circles to integers
                #circles = np.round(circles[0, :]).astype("int")
 
                # loop over the (x, y) coordinates and radius of the circles
                #for (x, y, r) in circles:
                    # draw the circle in the output image, then draw a rectangle
                    # corresponding to the center of the circle
                    #cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                    #cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
  
        
            # Erode
            erode_kernel = np.ones((3,3),np.uint8);
            eroded_img = cv2.erode(blurred,erode_kernel,iterations = 2)
        
            # dilate
            dilate_kernel = np.ones((7,7),np.uint8);
            dilated_img = cv2.dilate(eroded_img,dilate_kernel,iterations = 1)
        
            # Bitwise-AND mask and original image
            res = cv2.bitwise_and(frame,frame, mask=dilated_img)
        
            #cv2.imshow('Original',frame)
            cv2.imshow('Mask',mask)
            cv2.imshow('Gaussian Blur', blurred )
            cv2.imshow('Filtered Result',res)
            #cv2.imshow('resultat', np.hstack([frame, output]))
            #cv2.imshow('resultat', output)

            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break

        # close camera
        frame = balloon_video.close_camera()

        # close all windows
        cv2.destroyAllWindows()

# create global colour_finder object and run it
colour_finder = ColourFinder()
colour_finder.run()
