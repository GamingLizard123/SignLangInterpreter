import cv2
import mediapipe as mp

# Example function to map landmarks to different numbers based on handedness
def map_landmark_index(idx, handedness):
    if handedness == 'Left':
        # Define mapping for left hand landmarks (adjust as needed)
        left_hand_mapping = {
            0: 0,  
            1: 1,  
            2: 2,   
            3: 3,   
            4: 4,
            5: 5,
            6: 6,
            7: 7,
            8: 8,
            9: 9,
            10: 10,
            11: 11,
            12: 12,
            13: 13,
            14: 14,
            15: 15,
            16: 16,
            17: 17,
            18: 18,
            19: 19,
            20:20
        }
        return left_hand_mapping.get(idx, -1)  # Return mapped index or -1 for unknown indices
    elif handedness == 'Right':
        # Define mapping for right hand landmarks (adjust as needed)
        right_hand_mapping = {
            0: 21,  
            1: 22,  
            2: 23,   
            3: 24,   
            4: 25,
            5: 26,
            6: 27,
            7: 28,
            8: 29,
            9: 30,
            10: 31,
            11: 32,
            12: 33,
            13: 34,
            14: 35,
            15: 36,
            16: 37,
            17: 38,
            18: 39,
            19: 40,
            20:41
        }
        return right_hand_mapping.get(idx, -1)  # Return mapped index or -1 for unknown indices
    else:
        return -1  # Handle cases where handedness is not recognized

def printPositions(hand_landmarks, handedness):
    if hand_landmarks:
        for idx, landmark in enumerate(hand_landmarks.landmark):
            mapped_idx = map_landmark_index(idx, handedness)
            if mapped_idx != -1:
                print(f"{handedness} hand - Index {mapped_idx}: ({landmark.x}, {landmark.y}, {landmark.z})")

def runTracker():        
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_drawing = mp.solutions.drawing_utils

    # Initialize webcam
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame and detect hands
        result = hands.process(rgb_frame)

        # Draw hand landmarks
        if result.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
                # Determine handedness
                if result.multi_handedness:
                    handedness = result.multi_handedness[hand_idx].classification[0].label
                else:
                    handedness = 'Unknown'

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                printPositions(hand_landmarks, handedness)

                # Draw the landmarks with their indices
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    h, w, _ = frame.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    cv2.putText(frame, str(map_landmark_index(idx, handedness)), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

                
        # Display the frame
        cv2.imshow('Hand Tracker', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

runTracker()
