# Sign-Detection
Sign detection using nicla vision
Steps To Run 

1. Change WiFi credentials SSID , KEY to your WiFi name and password in main.py
2. Connect Nicla Vision and copy main.py and trained.tflite , labels.txt  in the Nicla Vision memory. 
3. To view the camera output with classification on web browser open the the following link http://192.168.243.41:8080/ where 192.168.243.41 is your Nicla Vision Ip address which can be obtained by any standard ip scanner. Alternatively, the ip can be viewed by running the code on OpenMv and opening serial monitor where the ip of Nicla Vision is displayed once connected to WiFi.

Models present:
2 tflite models are present in models directory. Model1.tflite consist of 10 classes where place identification boards are present . Model2.tflite consiste of 9 classes where place identification sign board is absent. Place Identification board was added for future scopre of OCR detection in sign boards. By default Model2.tflite is trained.tflite model stored in previous directory.

## Additional Info 
1. Device blinks blue light when connected to WiFi.
2. Device blinks yellow light when other device open the link to view camera output.
