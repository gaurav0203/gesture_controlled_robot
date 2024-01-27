# Gesture Controlled Robot

Use hand gestures to control the movement of the robotic car. The gesture detected by the camera determines the command to be sent to the car.
It can be also controlled through a webage on localhost

### Gesture Detection and Command Sending

### Robot Movement Video

### Webpage

![Webpage Controller](/Example/webpage.png)
> Webpage can we loaded on any device connected to the same wifi

### Circuit Connections:
- Attach Motors to Motor Driver
- Attach 9v Positive to 12v on Motor Driver and 9v Negative to GND on Motor Driver
- Attach IN1 to D1
- Attach IN2 to D2
- Attach IN3 to D6
- Attach IN4 to D7
- Attach 4.8v positive to VCC on Nodemcu and 4.8v negative to GND on Nodemcu
- Connect GND of Motor Driver and GND of Nodemcu 

### Controls:
- Left Index Finger Drives Left Motor Forward
- Right Index Finger Drives Right Motor Forward
- Left Index Finger and Left Middle Finger Drives Left Motor Backwards
- Right Index Finger and Right Middle Finger Drives Right Motor Backwards
- Both Index Fingers Drives Both Motors Forwards
- Both Index Fingers and Both Middle Fingers Drives Both Motors in Reverse

### Components :
- NodeMCU ESP8266
- L298 Motor Driver Moduule
- Metal Chassis
- 2 DC Motors with Wheels
- 9v Battery (to power the motors)
- 4 x 1.2v NiMH (to power the board)
- Breadboard
- Jumper Wires

### Instructions to use :
- Download this codes and install mediapipe and opencv-python
- Install Micropython on your ESP8266 Board
- Update the code (your ssid and password) in boot.py (located in ESP8266Code Folder)
- Update Pins if you are using different pins
- Upload the code in ESP9266Code folder to board using pymakr (VSCode Extension)
- Update the IP in recognizer.py
- If you go to IP of board in browser then the webpage to control the bot should load or you can directly control bot through gestures by running recognizer.py


