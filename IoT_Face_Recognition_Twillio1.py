from picamera2 import Picamera2, Preview
import face_recognition
from twilio.rest import Client
from time import sleep

# Twilio setup
account_sid = 'AC06f9e476a6cca0dcc68d3b571632660b'
auth_token = 'c71247cfd876f2787bfcfa68369f918f'
twilio_number = '+447893944454'
destination_number = '+447342953881'
client = Client(account_sid, auth_token)

def capture_image():
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
    picam2.configure(camera_config)
    picam2.start()

    picam2.start_preview(Preview.QTGL)
    sleep(5)  # Allow time for camera to focus

    # Capture and save the image
    image_path = '/home/pi/image.jpg'
    picam2.capture_file(image_path)
    print("Image Captured")

    picam2.stop_preview()
    picam2.close()
    return image_path

def detect_faces(image_path):
    # Load the captured image and known face image
    known_image = face_recognition.load_image_file("/path/to/known_face.jpg")
    known_encoding = face_recognition.face_encodings(known_image)[0]

    unknown_image = face_recognition.load_image_file(image_path)
    unknown_encodings = face_recognition.face_encodings(unknown_image)
    
    if unknown_encodings:
        result = face_recognition.compare_faces([known_encoding], unknown_encodings[0])
        return result[0]  # Return True if recognized, False otherwise
    return False

def send_sms(message):
    client.messages.create(
        body=message,
        from_=twilio_number,
        to=destination_number
    )
    print("SMS sent!")

# Main code
image_path = capture_image()
if not detect_faces(image_path):
    print("Unrecognized face detected.")
    send_sms("Alert: Unrecognized face detected.")
else:
    print("Face recognized.")
