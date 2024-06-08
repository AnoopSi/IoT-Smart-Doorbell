from gpiozero import MotionSensor
from picamera2 import Picamera2
import face_recognition
import time
from twilio.rest import Client

# Initialize the PIR sensor and Picamera2
pir = MotionSensor(4)
picam2 = Picamera2()

# Twilio setup
account_sid = 'your_account_sid'  # Replace with your Account SID
auth_token = 'your_auth_token'  # Replace with your Auth Token
twilio_number = 'your_twilio_number'  # Replace with your Twilio phone number
destination_number = 'destination_phone_number'  # Replace with the number to receive the SMS

client = Client(account_sid, auth_token)

# Path to the known face image
known_image = face_recognition.load_image_file("/path/to/known_face.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

def capture_image():
    picam2.start_preview()
    time.sleep(5)  # Camera focus time
    image = picam2.capture_array()
    picam2.stop_preview()
    return image

def detect_faces(image):
    unknown_encodings = face_recognition.face_encodings(image)
    if unknown_encodings:
        # For this prototype, we are assuming there's only one face, compare it to the known face
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

print("System armed, waiting for motion...")

while True:
    pir.wait_for_motion()
    print("Motion detected! Capturing image...")
    captured_image = capture_image()
    
    if not detect_faces(captured_image):
        print("Unrecognized")
        send_sms("Unrecognized face detected at your door.")
    
    pir.wait_for_no_motion()
