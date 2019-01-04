from django.shortcuts import render
from .forms import ConfigForm, SmptForm
#from .video_screening import signin #--> should use this import instead of creating this in the view
import configparser
import smtplib

# Create your views here.
def index(request):
    config = configparser.ConfigParser()
    config.read('webui/config.ini')

    config_dict = {'HISTORY': int(config['settings']['md_history']),
                   'THRESHOLD': int(config['settings']['md_threshold']),
                   'BASE_MOVEMENT_THRESHOLD': int(config['settings']['movement_detection_threshold']),
                   'OD_INTERVAL': int(config['settings']['od_frames']),
                   'CAMERA_IP_ADDRESS': config['settings']['camera_IP'],
                   'ALERT_ADDRESS': config['settings']['alert_address'],
                   'NOTIFY': config['settings']['notify']}

    form = ConfigForm
    logform = SmptForm

    if request.method == "GET":
        form = ConfigForm(initial=config_dict)
        logform = SmptForm()

    elif request.method == "POST":
        #Find which form is submitted using submit button name
        if 'smptlogin' in request.POST:
            logform = SmptForm(request.POST)
            form = ConfigForm(initial=config_dict)
            print("Logform initiated")

            if logform.is_valid():
                #try:
                    email_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    email_server.ehlo_or_helo_if_needed()
                    #email_server.starttls()
                    email_server.login(logform.cleaned_data['USERNAME'],logform.cleaned_data['PASSWORD'])
                    print("Login successful")
                #except:
                    #print("Not able to login") #Need to send this information back to the page

        elif 'setconfig' in request.POST:
            form = ConfigForm(request.POST)
            logform = SmptForm()
            print("Form initiated")

            print(form.is_valid())
            if form.is_valid():
                config.set('settings', 'md_history', str(form.cleaned_data['HISTORY']))
                config.set('settings', 'md_threshold', str(form.cleaned_data['THRESHOLD']))
                config.set('settings', 'movement_detection_threshold', str(form.cleaned_data['BASE_MOVEMENT_THRESHOLD']))
                config.set('settings', 'od_frames', str(form.cleaned_data['OD_INTERVAL']))
                config.set('settings', 'camera_IP', form.cleaned_data['CAMERA_IP_ADDRESS'])
                config.set('settings', 'alert_address', form.cleaned_data['ALERT_ADDRESS'])
                config.set('settings', 'notify', str(form.cleaned_data['NOTIFY']))

                with open('webui/config.ini', 'w') as configfile:
                    config.write(configfile)
                    print('Write completed')


    return render(request, 'index.html', {'form': form, 'logform': logform})

#def run_analyzer(request):
    #run analyzer here
