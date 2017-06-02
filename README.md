# OpenTracker
QuadCopter Object Tracking on a budget.

This project is a variation of the original Rand'ys Red Balloon Finder implementation.
Based on this blog : http://diydrones.com/profiles/blogs/red-balloon-finder , I modified the Python scripts
making now possible to test on any ArduPilot based Quadcopter on a low budget , relatively easy to implement controler.

How does it work ?
Using a Companion Computer -Raspberry Pi Zero - and Drone Kit Python, we are switching to GUIDED mode so that we are controlling an ArduPilot based Flight Controler - Pixracer - to rotate the copter slowly around while it  receives on serial port the  coordonates of a  detected object from  the OpenMV camera x-y plane . During the search it keeps track of the 'best' object it saw so after the copter has rotate 360 degrees it sends commands to point the vehicle in the direction of that object  and then sends 3D velocity requests, up to 15 times per second to guide the copter towards the top of target.   On the actual release , the mission is to  chase a red balloon and fly on top of it in order to burst it with sharp objects attached to the landig gears, once its passed the balloon, the OpenMV camera system is losing track of the object and the python script  resume control back to LOITER, making it ready to repeat the mission once we switch back to GUIDED.
What do we need?
OpenMV- M7  Machine Vision system (55$)
RaspberryPi Zero (5$)
USB to Serial (FTDI) adapter and cables (5$)
DroneKit Python
Python Script
OpenMV Script
Total Bill of Material = 65$

OpenMV
https://openmv.io/
The OpenMV Cam  M7 is powered by the 216 MHz ARM Cortex M7 processor, enabling 640x480 grayscale images / video (up to 320x240 for RGB565 still) with a camera on board that you program in Python. They make it easy to run machine visions algorithms on what the OpenMV Cam sees so you can track colors, detect faces, and more in seconds and then control I/O pins in the real-world.

Raspberry Pi Zero
We are using the basic Pi Zero on this system , we dont need additionnal connectivity except for the USB to Serial adapter. The RPI Zero is running with the standard Graphuical User Interface9GUI)  Raspian OS that you can downlad here: https://www.raspberrypi.org/documentation/installation/installing-images/README.md   with the Python DroneKit installed http://python.dronekit.io/guide/quick_start.html#installation. We need to get the console disabled in order to access the serial ports, generally it done by editing the /boot/cmdline.txt file and enabling the serial port. Please note that I am running the full desktop image , making it easy to develop in a GUI environment and then switch back to console only for flyin using  raspi-config.


Python Scripting
Based on the original code, https://github.com/rmackay9/ardupilot-balloon-finder, lets take a look inside :

On the main script, Balloon_strategy.py , there are some important features you need to know (# means comment):
from pymavlink import mavutil
from dronekit import connect, VehicleMode, LocationGlobal
		#We need these modules (installed with deonekit ) to control vehicle
import balloon_config
	  	#This is the configuration script, allowing usage the configuration file 
  # connect to vehicle with dronekit
		#Using default parameter or specific from the balloon_finder.cnf
#MAIN
            # only process images once home has been initialised
            if self.check_home():

                # check if we are controlling the vehicle
                self.check_status()

                # look for balloon in image
                self.analyze_image()

                # search or move towards balloon
                if self.search_state > 0:
                    # search for balloon
                    self.search_for_balloon()
                else:
                    # move towards balloon
                    self.move_to_balloon()
    # complete - balloon strategy has somehow completed so return control to the autopilot           
        # stop the vehicle and give up control
        # if in GUIDED mode switch back to LOITER
