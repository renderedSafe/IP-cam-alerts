from django import forms

class ConfigForm(forms.Form):
    HISTORY                 = forms.IntegerField()
    THRESHOLD               = forms.IntegerField()
    BASE_MOVEMENT_THRESHOLD = forms.IntegerField()
    OD_INTERVAL             = forms.IntegerField()
    CAMERA_IP_ADDRESS       = forms.CharField()
    ALERT_ADDRESS           = forms.EmailField(required=False)
    NOTIFY                  = forms.BooleanField(required=False)

class SmptForm(forms.Form):
    USERNAME = forms.CharField(required=False)
    PASSWORD = forms.CharField(max_length=32, widget=forms.PasswordInput, required=False)
