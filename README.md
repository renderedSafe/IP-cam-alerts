# IP-cam-alerts
IP camera motion SMS alerts screened with object detection to reduce false-positives. 

Forked from @renderedSafe in order to add Django web interface for streamlining configuaration and setup

This program works by grabbing frames continuously from an IP camera in a parallel loop, and checks the most recent frame for motion every half-second. If and when it detects motion, it runs a set number of subsequent frames through an object detector, and if it detects a person, it sends a text or email with images of each frame that had a person in it attached. 

The sensetivity of the motion detector and the number of frames to run object detection on post motion-detection are configurable in the config file. 

To use:
1. Add an address for an IP camera in the spot for it in the config.ini
2. Add an address to send alerts to in the same file
3. Add a directory named 'models', and in it put the YOLOv3 model you can download here: https://github.com/OlafenwaMoses/ImageAI/releases/tag/1.0/


Dependencies:

-opencv-python

-numpy

-ImageAI

For django requirements:
cd to ip-cam-alerts
pip install -r requiremennts.txt
