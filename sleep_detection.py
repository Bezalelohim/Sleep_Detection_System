import cv2
import mediapipe as mp
import numpy as np
import time
from gpiozero import Buzzer
from eye_aspect_ratio import calculate_ear
from vehicle_control import VehicleController
from alert_system import AlertSystem

class DriverMonitoringSystem:
    def __init__(self):
        # Initialize MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Initialize camera (CSI camera for Raspberry Pi)
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Initialize components
        self.buzzer = Buzzer(17)  # GPIO pin 17
        self.vehicle_controller = VehicleController()
        self.alert_system = AlertSystem(self.buzzer)
        
        # Constants
        self.EAR_THRESHOLD = 0.25
        self.CONSECUTIVE_FRAMES = 20
        self.DROWSY_TIME = 2.0  # seconds
        
        # Variables for tracking
        self.drowsy_counter = 0
        self.last_alert_time = time.time()
        self.emergency_mode = False

    def process_frame(self, frame):
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Calculate EAR for both eyes
                left_ear = calculate_ear(face_landmarks, "left")
                right_ear = calculate_ear(face_landmarks, "right")
                ear = (left_ear + right_ear) / 2.0
                
                # Check for drowsiness
                if ear < self.EAR_THRESHOLD:
                    self.drowsy_counter += 1
                    if self.drowsy_counter >= self.CONSECUTIVE_FRAMES:
                        self.handle_drowsiness()
                else:
                    self.drowsy_counter = 0
                    self.emergency_mode = False
                
                # Draw facial landmarks
                self.draw_landmarks(frame, face_landmarks)
        
        return frame

    def handle_drowsiness(self):
        current_time = time.time()
        
        # First level alert - just buzzer
        if not self.emergency_mode:
            self.alert_system.trigger_alert()
            
        # Second level - emergency procedures
        if current_time - self.last_alert_time > self.DROWSY_TIME:
            self.emergency_mode = True
            self.vehicle_controller.initiate_emergency_stop()
            self.alert_system.trigger_emergency_alert()
            self.last_alert_time = current_time

    def draw_landmarks(self, frame, landmarks):
        for landmark in landmarks.landmark:
            x = int(landmark.x * frame.shape[1])
            y = int(landmark.y * frame.shape[0])
            cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

    def run(self):
        try:
            while True:
                ret, frame = self.camera.read()
                if not ret:
                    break
                
                processed_frame = self.process_frame(frame)
                cv2.imshow('Driver Monitoring System', processed_frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        finally:
            self.camera.release()
            cv2.destroyAllWindows()
            self.face_mesh.close()

if __name__ == "__main__":
    monitoring_system = DriverMonitoringSystem()
    monitoring_system.run() 