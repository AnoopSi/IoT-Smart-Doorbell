# capture_image_picamera2.py
from picamera2 import Picamera2, 
from time import sleep

# Initialize Picamera2
picam2 = Picamera2()

# Configure and start the camera
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display= "lores")
picam2.configure(camera_config)
picam2.start()

# Start preview for focusing
picam2.start_preview(Preview.QTGL)
picam2.start()
sleep(5)  # Time for the camera to focus

# Capture the image
picam2.capture_file('/home/pi/image.jpg')
print("Image Captured")

# Stop the preview and close the camera
picam2.stop_preview()
picam2.close()

# This code is to save known face. Change the path to location of Know face.
