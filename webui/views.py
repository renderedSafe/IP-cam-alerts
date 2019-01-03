from django.shortcuts import render
from .forms import ConfigForm, SmptForm
import configparser

# Create your views here.
def index(request):
    config = configparser.ConfigParser()
    config.read('webui/config.ini')

    if request.method == "GET":
        config_dict = {'HISTORY': int(config['settings']['md_history']),
                       'THRESHOLD': int(config['settings']['md_threshold']),
                       'BASE_MOVEMENT_THRESHOLD': int(config['settings']['movement_detection_threshold']),
                        'OD_INTERVAL': int(config['settings']['od_frames']),
                        'CAMERA_IP_ADDRESS': config['settings']['camera_IP'],
                        'ALERT_ADDRESS': config['settings']['alert_address'],
                        'NOTIFY': config['settings']['notify']}

        form = ConfigForm(initial=config_dict)
        logform = SmptForm()

    elif request.method == "POST":
        form = ConfigForm(request.POST)

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
        #if form.is_valid():


    return render(request, 'index.html', {'form': form, 'logform': logform})

#def run_analyzer(request):
    #run analyzer here
