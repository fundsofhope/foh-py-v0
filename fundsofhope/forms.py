from django import forms


class UploadImageForm(forms.Form):
    picture = forms.ImageField()
    id = forms.IntegerField()
