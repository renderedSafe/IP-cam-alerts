
IP-cam-alerts
IP camera motion SMS alerts screened with object detection to reduce false-positives.

This program works by grabbing frames continuously from an IP camera in a parallel loop, and checks the most recent frame for motion every half-second. If and when it detects motion, it runs a set number of subsequent frames through an object detector, and if it detects a person, it sends a text or email with images of each frame that had a person in it attached.

!['Demo text alert image](https://github.com/renderedSafe/IP-cam-alerts/blob/master/Screenshot_20190105-223219.png?raw=true)

The sensetivity of the motion detector and the number of frames to run object detection on post motion-detection are configurable in the config file.

To use:

Easy way for Windows users:

1. Download the windows-executable folder
2. Open config.ini with a text editor. Go to the bottom of the file and find the spots for the alert address and IP camera address and add that info in. For an IP camera, Google how to find the RTSP address for your camera and put that address in the spot for the camera address. Save the file
3. ~~Download one of the YOLO models from this link: https://github.com/OlafenwaMoses/ImageAI/releases/tag/1.0/. Add it into the models folder of the windows-executable directory you downloaded. (The default model for the program is yolo-tiny.h5, so unless you change it in config.ini, use that one).~~ Model files now included. No step needed here.
4. Run video_screening.exe. A terminal window should appear. Follow the prompts, the email you enter will be the one from which the alerts are sent. 
5. Sit back and wait for the alert texts. 


For other users/those who just want to run the Python script:

1. Add an address for an IP camera in the spot for it in the config.ini
2. Add an address to send alerts to in the same file
3. Add a directory named 'models', and in it put the YOLOv3 and/or yolo-tiny model you can download here (yolo-tiny is set as default in config.ini. You can change that): https://github.com/OlafenwaMoses/ImageAI/releases/tag/1.0/
(Or just copy the models directory into the base directory, it has the model files in it.)

(Freeze support is enabled in the script, but you may need to add the ffmpeg .dll file from the cv2 site package in your python directory. See this SO question: https://stackoverflow.com/questions/44415424/videocapture-opencv-python-pyinstaller-not-opening.)


Dependencies:

-opencv-python

-numpy

-ImageAI
