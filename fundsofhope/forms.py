from django import forms


class UploadFileForm(forms.Form):
    picture = forms.ImageField()
    id = forms.IntegerField()
