from django.test import TestCase
from video_screening.py import main

# Create your tests here.

def test_main():
    from video_screening.py import main
    
    print("Calling main...")
    main()
    print("Main called successfully")

"""
def test_smtp():
    import smtplib

    email_server = smtplib.SMTP('smtp.gmail.com', 587)
    email_server.starttls()
    email_server.login(username, password)
"""

def test_configparser():
    import configparser

    config = configparser.ConfigParser()
    config.read('webui/config.ini')

#test_configparser()
main()
