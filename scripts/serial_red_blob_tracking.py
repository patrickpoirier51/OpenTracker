import image, math, pyb, sensor, struct, time
uart_baudrate = 9600
uart = pyb.UART(3, uart_baudrate, timeout_char = 1000)
clock = time.clock()


lens_mm = 2.8
lens_to_camera_mm = 22
sensor_w_mm = 3.984
sensor_h_mm = 2.952
x_res = 320
y_res = 240
f_x = (lens_mm / sensor_w_mm) * x_res
f_y = (lens_mm / sensor_h_mm) * y_res
c_x = x_res / 2
c_y = y_res / 2
h_fov = 2 * math.atan((sensor_w_mm / 2) / lens_mm)
v_fov = 2 * math.atan((sensor_h_mm / 2) / lens_mm)


threshold_index = 0 # 0 for red, 1 for green, 2 for blue

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track in general red/green/blue things. You may wish to tune them...
thresholds = [(52, 73, 11, 102, 28, 74), # generic_red_thresholds
              (30, 100, -64, -8, -32, 32), # generic_green_thresholds
              (0, 30, 0, 64, -128, 0)] # generic_blue_thresholds

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(30)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking



# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. "merge=True" merges all overlapping blobs in the image.

while(True):
        clock.tick()
        start = pyb.millis()
        img = sensor.snapshot()
        for blob in img.find_blobs([thresholds[threshold_index]], pixels_threshold=100, area_threshold=100, merge=False):
              img.draw_rectangle(blob.rect())
              img.draw_cross(blob.cx(), blob.cy())
              timer = int (start)

              print("TRACK %f %f " % (blob.cx(), blob.cy()), blob.w(),blob.h())

              uart.write("%d ; %d ; %d ; %d \r\n " % (blob.cx(), blob.cy(),blob.w(),blob.h()))

              #print("FPS %f" % clock.fps())
