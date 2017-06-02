# OpenTracker
QuadCopter Object Tracking on a budget.

This project is a variation of the original Rand'ys Red Balloon Finder implementation.
Based on this blog : http://diydrones.com/profiles/blogs/red-balloon-finder , I modified the Python scripts
making now possible to test on any ArduPilot based Quadcopter on a low budget , relatively easy to implement controler.

How does it work ?
Using a Companion Computer -Raspberry Pi Zero - and Drone Kit Python, we are switching to GUIDED mode so that we are controlling an ArduPilot based Flight Controler - Pixracer - to rotate the copter slowly around while it  receives on serial port the  coordonates of a  detected object from  the OpenMV camera x-y plane . During the search it keeps track of the 'best' object it saw so after the copter has rotate 360 degrees it sends commands to point the vehicle in the direction of that object  and then sends 3D velocity requests, up to 15 times per second to guide the copter towards the top of target.   On the actual release , the mission is to  chase a red balloon and fly on top of it in order to burst it with sharp objects attached to the landig gears, once its passed the balloon, the OpenMV camera system is losing track of the object and the python script  resume control back to LOITER, making it ready to repeat the mission once we switch back to GUIDED.

OpenMV
https://openmv.io/
The OpenMV Cam  M7 is powered by the 216 MHz ARM Cortex M7 processor, enabling 640x480 grayscale images / video (up to 320x240 for RGB565 still) with a camera on board that you program in Python. They make it easy to run machine visions algorithms on what the OpenMV Cam sees so you can track colors, detect faces, and more in seconds and then control I/O pins in the real-world.

Raspberry Pi Zero
We are using the basic Pi Zero on this system , we dont need additionnal connectivity except for the USB to Serial adapter. The RPI Zero is running with the standard Graphuical User Interface9GUI)  Raspian OS that you can downlad here: https://www.raspberrypi.org/documentation/installation/installing-images/README.md   with the Python DroneKit installed http://python.dronekit.io/guide/quick_start.html#installation. We need to get the console disabled in order to access the serial ports, generally it done by editing the /boot/cmdline.txt file and enabling the serial port. Please note that I am running the full desktop image , making it easy to develop in a GUI environment and then switch back to console only for flyin using  raspi-config.


Python Scripting
Based on the original code, https://github.com/rmackay9/ardupilot-balloon-finder, lets take a look inside :
On your RPI, open a terminal window  and git clone OpenTracker

With an editor (simply open the file with the file manager), adjust the parameters of ballloon_finder.cnf , if required.
You can test if the OpenMV to RPI Zero connection is working correctly by launching OpenMV.py using command line : sudo python openmv.py or using IDLE2 editor and running script. Please note that you have to remove the # before print command in order to see the values on console. Please note that generally you do not need to run commands with sudo but it might happen sometimes that you dont have all the privilidge to access codes and devices, anyway its up to each users to test with or without sudo.

Hint: 
Ckeck for activity light on FTDI  (Show / Hide object) == Knowing the pattern will be helpfull once you are testing live

Once completed, comment out the print command, save and you are ready for test.


OpenMV script
Open IDE
Load the Script
Adjut the color filter using  Tools/Machine Vision/ Threshold editor
Make sure you are using LAB color space
Cut the Values & Paste them in  the appropriate filter (Red our Example) for your object
please note in the lab that I am using a small red ''stress ball'' for tests.
Run the test and confirm that it is tracking steadily
When satisfied, Tools/Save Open script to OpenMV 


Testing in SITL
Practice makes good and using SITL may save your day ;-)
Leaving the
You can connect the RPI Zero Ftdi Usb to Serial converter to a  second FTDI  USB to serial  on a  Linux based computer (dont forget to cross the XMIT to RX(
Launch SITL:
/home/Ardupilot\ArduCopter/$ sim_vehicle.py --console --map --aircraft=balloon --out udp:missopn.planner.pc.adress:14550 --out /dev/ttyUSB0,115200

On the RPI start the Tracker on within a terminal session with sudo python balloon_strategy.py or using IDLE2 editor and running script
You should see on the RPI console  the connection to vehicle, the parameters  initialisation sequence and the tracker waiting for command.

On SITL you can initiate this sequence:
⦁	mode loiter
⦁	arm Throttle
⦁	rc 3 1800
⦁	takeoff 30  	(wait until it reach this altitude)
⦁	 rc 3 1500  	(so it keep altitude in LOITER)
⦁	mode guided

 Once in guided, the RPI takes command and you will see the quadcopter start turning, serching for the object.
You can test by ''showing'' the object to the camera for a brief period of time, and you should see the "  "Found Balloon at heading:%f Alt:%f Dist:%f"  " message appearing.  Hide the object and wait until the message "Balloon was near expected heading, finalising yaw to %f" message appers , starting the final alignment to object , and then you can ''show'' the object  and start chasing when you see "Finalised yaw to %f, beginning run"

Now, the  simulated vehicle will  follow the object on the camera, Looking at the OpenMV IDE you will be able to judge if the simulator react accordingly to the target position on the camera screen. Basically the vehicle will move left-right and up-down (altitude) according to where the object is located in reference to the center of the camera, if its dead center, the simulated quadcopter  should go straight witn no altitude change.

If you hide the object:
 # if we lose sight of a balloon for this many seconds we will consider it lost and give up on the search
 self.lost_sight_timeout = 3
 the tracker will give up : "Lost Balloon, Giving up"
and will go through this sequence:
# complete - balloon strategy has somehow completed so return control to the autopilot          
# stop the vehicle and give up control
# if in GUIDED mode switch back to LOITER

Once  in LOITER  you can run anoter test just by switching back to GUIDED.
