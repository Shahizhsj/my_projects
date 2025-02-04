import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


points = []
total_distance = 0
measurement_done = False

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
distance_cm = 0

with mp_hands.Hands(static_image_mode=False,
                    max_num_hands=2,
                    min_detection_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        
        if results.multi_hand_landmarks and results.multi_handedness:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                
                handedness = results.multi_handedness[idx].classification[0].label
                if handedness == "Left":  
                    
                    index_tip = hand_landmarks.landmark[8]
                    middle_tip = hand_landmarks.landmark[12]
                    ring_tip = hand_landmarks.landmark[16]
                    
                    
                    h, w, _ = frame.shape
                    x_index, y_index = int(index_tip.x * w), int(index_tip.y * h)
                    x_middle, y_middle = int(middle_tip.x * w), int(middle_tip.y * h)
                    x_ring, y_ring = int(ring_tip.x * w), int(ring_tip.y * h)
                    
                    
                    if (y_index < y_middle) and (abs(y_index - y_middle) > 10):
                        measurement_done = False  # Reset measurement flag if drawing resumes
                        
                        # Draw a circle at the index finger tip
                        cv2.circle(frame, (x_index, y_index), 10, (0, 255, 0), -1)
                        
                        # Append the current position to the list of points
                        if len(points) == 0:
                            points.append([x_index, y_index])
                        else:
                            # Draw a line from the last point to the current point
                            cv2.line(frame, (points[0][0], points[0][1]), (x_index, y_index), (230, 230, 240), 10)
                            points.append([x_index, y_index])
                            
                   
                    elif ( y_middle<y_ring) and (abs(y_middle-y_ring)>10):
                        if points and not measurement_done:
                            # Calculate the total drawn distance (in pixels)
                            total_distance = 0
                            for i in range(len(points) - 1):
                                dist = math.sqrt(
                                    (points[i+1][0] - points[i][0]) ** 2 +
                                    (points[i+1][1] - points[i][1]) ** 2
                                )
                                total_distance += dist
                            
                            # Convert pixels to centimeters (adjust this factor after calibration)
                            cm_per_pixel = 8 / 40  # Example conversion factor
                            distance_cm = total_distance * cm_per_pixel
                            
                            measurement_done = True  # Avoid repeated calculations
                            
                            # Display measurement on the frame
                            cv2.putText(frame, f"Total Distance: {int(distance_cm)} cm", 
                                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                                        0.8, (0, 255, 255), 2)
                    else:
                        # If the hand is in a neutral position, reset the drawing
                        points = []
                        total_distance = 0
                        distance_cm = 0
                        measurement_done = False
                        print("Hello")
                        

                    # Optionally, draw the hand landmarks for debugging
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Always display the current distance (if measured)
        cv2.putText(frame, f"Total Distance: {int(distance_cm)} cm", 
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.8, (0, 255, 255), 2)      
                    
        cv2.imshow("Left Hand Index Finger Tracking", frame)

        # Exit when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
