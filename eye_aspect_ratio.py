import numpy as np

def calculate_ear(landmarks, eye_side):
    # MediaPipe facial landmarks for eyes
    if eye_side == "left":
        points = [33, 160, 158, 133, 153, 144]  # Left eye landmarks
    else:
        points = [362, 385, 387, 263, 373, 380]  # Right eye landmarks
    
    # Get coordinates
    coords = []
    for point in points:
        landmark = landmarks.landmark[point]
        coords.append([landmark.x, landmark.y])
    
    coords = np.array(coords)
    
    # Calculate distances
    vertical_1 = np.linalg.norm(coords[1] - coords[5])
    vertical_2 = np.linalg.norm(coords[2] - coords[4])
    horizontal = np.linalg.norm(coords[0] - coords[3])
    
    # Calculate EAR
    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
    return ear 