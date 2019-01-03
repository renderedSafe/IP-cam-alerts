import sched, time
import cv2
import numpy as np
from collections import deque
from imageai.Detection import ObjectDetection
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from PIL import Image
import io
import getpass
from multiprocessing import Process, Queue
import configparser

############################################################################
#######################Configuring settings from config.ini#################
config = configparser.ConfigParser()
config.read('webui/config.ini') #might work

# Settings for the motion detector
HISTORY = int(config['settings']['md_history'])
THRESHOLD = int(config['settings']['md_threshold'])
# Threshold number for movement to be detected
BASE_MOVEMENT_THRESHOLD = int(config['settings']['movement_detection_threshold'])
# Number of frames to detect objects in after movement is first detected
OD_INTERVAL = int(config['settings']['od_frames'])
#IP address of the camera
# TODO: Unfuck this. split this value into username, password, and IP, then concat so we can grab the password securely
CAMERA_IP_ADDRESS = config['settings']['camera_IP']
ALERT_ADDRESS = config['settings']['alert_address']
NOTIFY = config['settings']['notify']
#############################################################################



def getFrames(q):
    """
    This function is meant to be run as a multiprocessing Process object
    :param q: multiprocessing.Queue object
    :return: access q from outside funtction
    """
    cap = cv2.VideoCapture(CAMERA_IP_ADDRESS)
    frame_time = time.time()
    while True:
        ret, frame = cap.read()
        if q.qsize() >= 5:
            q.get()

        q.put(frame)
        # try:
        #     print(f'Frames grabbed per second: {1 / (time.time() - frame_time)}')
        # except ZeroDivisionError as e:
        #     print(e)
        frame_time = time.time()

def detectMovement(frame):
    """
    Detects movement in frame supplied by checking against the last few frames

    :param frame: numpy array of the frame to be processed
    :return boolean: True if movement detected above specified threshold, else, false
    """
    fg_mask = bg_subtractor.apply(frame)
    total_movement = int(np.sum(fg_mask == 255))
    #print(f'Movement level: {total_movement}')

    return total_movement > BASE_MOVEMENT_THRESHOLD

def findObjects(frame):
    """
    Detects objects in the supplied frame

    :param frame: numpy array of an image.
    :return (debugging_image, objects_detected): a tuple, (<a numpy array image with detections>,
                                                            <a list of objects detected >).
    """
    #smaller image makes for faster detection
    frame = cv2.resize(frame, (640, 360))
    start_time = time.time()
    debugging_image, detections = detector.detectObjectsFromImage(frame, input_type="array", output_type="array",
                                                                 minimum_percentage_probability=40)
    objects_detected = [item['name'] for item in detections]
    print(f'Detected the following objects: {objects_detected}')
    finish_time = time.time()
    total_time = finish_time - start_time
    print(f'Took {total_time} seconds to detect objects')

    return debugging_image, objects_detected

def sendAlertEmail(image_list, detections):

    msg = MIMEMultipart()
    msg['Subject'] = 'Object of interest detected'
    msg['From'] = username
    msg['To'] = ALERT_ADDRESS

    msg_text = MIMEText(f'Objects detected:{detections}')
    msg.attach(msg_text)

    image_number = 1
    for image in image_list:
        image = cv2.imencode('.jpeg', image)[1]
        image = image.tobytes()
        msg_image = MIMEImage(image, name='image')
        msg_image.add_header('Content-ID', f'<image{image_number}>')
        msg_image.add_header('Content-Disposition', 'inline')
        msg.attach(msg_image)
        image_number += 1


    email_server.send_message(msg, username, ALERT_ADDRESS)

def objectDetectionLoop(frame):
    image_list = []  # A list to keep images in that have had objects detected in them
    od_start_time = time.time()
    total_detections = []
    for i in range(OD_INTERVAL):
        detect_frame = frame_queue.get()  # This grabs a frame to be processed from the queue being stocked
        detection_image, detection_list = findObjects(detect_frame)  # This is the actual object detection
        od_start_time = time.time()
        total_detections.append(detection_list)
        print(f'Detection  on frame #{i+1}')
        if 'person' in detection_list:  # If there were any objects detected in that frame we shrink it and add it to the list
            image_list.append(detection_image)
            
    # If any images were added to the list, that means things were detected, and you should send the alert
    if image_list and NOTIFY == "True":
        print(f'Sending alert email with {len(image_list)} images attached')
        sendAlertEmail(image_list, set(total_detections))  #converting list to set to only send unique items

def analyzeVideo():
    # let's just grab the first frame before things get ahead of themselves
    ret, frame = cap.read()
    start_time = time.time()
    while True:
        cv2.imshow('image', frame)
        frame = frame_queue.get()

        fps = 1 / (time.time() - start_time)
        start_time = time.time()

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, f'FPS: {fps}', (0, 30), font, 1, (200, 255, 155), 2, cv2.LINE_AA)
        if detectMovement(frame):
            # annotate movement detection on the frame to be displayed
            cv2.putText(frame, 'MOVEMENT', (0, 400), font, 3, (0, 0, 255), 5, cv2.LINE_AA)
            cv2.putText(frame, 'DETECTED', (0, 500), font, 3, (0, 0, 255), 5, cv2.LINE_AA)

            # detecting the next OD_INTERVAL number of frames after motion detection
            print('Motion detected.')
            objectDetectionLoop(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            stream_process.terminate()
            break
        time.sleep(.5)

def main():
    config = configparser.ConfigParser()
    config.read('webui/config.ini') #might work

    # Settings for the motion detector
    global HISTORY = int(config['settings']['md_history'])
    global THRESHOLD = int(config['settings']['md_threshold'])
    # Threshold number for movement to be detected
    global BASE_MOVEMENT_THRESHOLD = int(config['settings']['movement_detection_threshold'])
    # Number of frames to detect objects in after movement is first detected
    global OD_INTERVAL = int(config['settings']['od_frames'])
    #IP address of the camera
    # TODO: Unfuck this. split this value into username, password, and IP, then concat so we can grab the password securely
    global CAMERA_IP_ADDRESS = config['settings']['camera_IP']
    global ALERT_ADDRESS = config['settings']['alert_address']
    global NOTIFY = config['settings']['notify']

    #
    # Send this information from the login form
    #
    #username = input('Email address for sending email: ')
    #password = input('Password:')

    cap = cv2.VideoCapture(CAMERA_IP_ADDRESS)

    # setting up the object detector
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join('models', 'yolo.h5'))
    detector.loadModel(detection_speed='fast')
    bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=HISTORY,
                                                       varThreshold=THRESHOLD)  # includes params from settings
    if notify == "True": #Might have to state that notify is a string
        email_server = smtplib.SMTP('smtp.gmail.com', 587)
        email_server.starttls()
        email_server.login(username, password)

    # setting up the queue that will be used to get data from the stream processing
    frame_queue = Queue(maxsize=10)
    # starting the stream processing multiprocess
    stream_process = Process(target=getFrames, args=(frame_queue,))
    stream_process.start()

    analyzeVideo()
