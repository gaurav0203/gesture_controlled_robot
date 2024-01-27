import cv2
import mediapipe as mp
import requests

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_command = "nothing"

# Modify the IP 
target_url = "http://192.168.0.102/?cmd="

def draw_connections(frame,landmark_list):
    image_height, image_width, _ = frame.shape
    prev_coordinates = landmark_list[0]

    for coordinates in landmark_list:
        if coordinates != prev_coordinates:
            frame = cv2.line(frame, (int(prev_coordinates.x * image_width),int(prev_coordinates.y * image_height)), (int(coordinates.x * image_width),int(coordinates.y * image_height)), (255,255,255),3)
            # print(prev_coordinates, coordinates)
            prev_coordinates = coordinates
        frame = cv2.circle(frame,(int(coordinates.x * image_width),int(coordinates.y * image_height)),5,(0,0,255),-1)
    

    return frame

def detect_command(left_hand_detection_flag, right_hand_detection_flag,left_hand_landmarks, right_hand_landmarks):
    left_index_finger_status = "down"
    left_middle_finger_status = "down"
    right_index_finger_status = "down"
    right_middle_finger_status = "down"

    if left_hand_detection_flag:
        left_index_finger_status = finger_up_detector(left_hand_detection_flag,left_hand_landmarks[0])
        left_middle_finger_status = finger_up_detector(left_hand_detection_flag,left_hand_landmarks[1])
    if right_hand_detection_flag:
        right_index_finger_status = finger_up_detector(right_hand_detection_flag,right_hand_landmarks[0])
        right_middle_finger_status = finger_up_detector(right_hand_detection_flag,right_hand_landmarks[1])

    command = "stop"

    #print(left_index_finger_status,left_middle_finger_status)
    #print(right_index_finger_status,right_middle_finger_status)

    if left_index_finger_status == "up":
        if right_index_finger_status == "up":
            if left_middle_finger_status == "up" and right_middle_finger_status == "up":
                command = "both_reverse"
            elif left_middle_finger_status == "down" and right_middle_finger_status == "down":
                command = "both_forward"
        elif left_middle_finger_status == "up":
            command = "left_reverse"
        elif left_middle_finger_status == "down":
            command = "left_forward"
    elif right_index_finger_status == "up":
        if right_middle_finger_status == "up":
            command = "right_reverse"
        elif right_middle_finger_status == "down":
            command = "right_forward"
    else:
        command = "stop"
        
    return command
    
    
def finger_up_detector(hand_presence, finger_landmarks):
    if hand_presence:
        prev_landmark_y_coordinate = -1.00
        for finger_landmark in finger_landmarks:
            if finger_landmark.y <= prev_landmark_y_coordinate:
                return "down"
            else:
                prev_landmark_y_coordinate = finger_landmark.y
        return "up"
    else:
        return "down"

while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        break
    
    # mirroring the frame
    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    
    results = hands.process(rgb_frame)

    left_hand_detection_flag = False
    right_hand_detection_flag = False
        
    left_hand_landmarks = []
    right_hand_landmarks = []
        

    if results.multi_hand_landmarks:    # Number of hands
                
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            handedness = results.multi_handedness[idx].classification[0].label
            handedness_score = results.multi_handedness[idx].classification[0].score

            
            index_finger_landmarks = [
                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP],
                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP],
                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP],
            ]

            middle_finger_landmarks = [
                hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP],
                hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP],
                hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP],
            ]
            #print(index_finger_landmarks)
            if handedness == "Left" and handedness_score > 0.90:
                left_hand_detection_flag = True
                left_hand_landmarks = [index_finger_landmarks, middle_finger_landmarks]
            if handedness == "Right" and handedness_score > 0.90:
                right_hand_detection_flag = True
                right_hand_landmarks = [index_finger_landmarks, middle_finger_landmarks]

            frame = draw_connections(frame, index_finger_landmarks)
            frame = draw_connections(frame, middle_finger_landmarks)

    
    
    new_command = detect_command(left_hand_detection_flag, right_hand_detection_flag,left_hand_landmarks, right_hand_landmarks)

    if prev_command != new_command:
                # commander logic
        url_command = ""
        
        if new_command == "left_forward":
            url_command = "lf"
        elif new_command == "left_reverse":
            url_command = "lr"
        elif new_command == "right_forward":
            url_command = "rf"
        elif new_command == "right_reverse":
            url_command = "rr"
        elif new_command == "both_forward":
            url_command = "bf"
        elif new_command == "both_reverse":
            url_command = "br"
        elif new_command == "stop":
            url_command = "sp"
        else:
            url_command = "sp"

        try:
            response = requests.get(target_url+url_command)
            print("--------")
            print(response.status_code)
            print("--------")
            if response.status_code == 200:
                print(f'{new_command} request sent')
            else:
                print(f'Failed to send {new_command} request. Status code: {response.status_code}')
        except requests.RequestException as e:
            print(f'Error sending request: {e}')
        print(new_command)

        prev_command = new_command

    
    cv2.imshow("Hand Lankmarks", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


