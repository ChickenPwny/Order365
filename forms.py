from django import forms
from .models import *

class BinderForm(forms.ModelForm):
    class Meta:
        model = Binder
        fields = ['name']  # remove 'user' from here

    def __init__(self, *args, **kwargs):
        super(BinderForm, self).__init__(*args, **kwargs)
        self.fields['user'] = forms.ModelChoiceField(queryset=User.objects.all())

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'user']  # specify 'name' and 'user' fields
        widgets = {
            'binderId': forms.HiddenInput(),  # Hide the BinderID field
        }

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'user', 'file']
        
class ProcessForm(forms.Form):
    action = forms.CharField(max_length=10, initial='process', widget=forms.HiddenInput())
    pk = forms.IntegerField(widget=forms.HiddenInput())

class DeleteForm(forms.Form):
    action = forms.CharField(max_length=10, initial='delete', widget=forms.HiddenInput())
    pk = forms.IntegerField(widget=forms.HiddenInput())

class ProcessSinglesForm(forms.Form):
    action = forms.CharField(max_length=10, initial='processSingles', widget=forms.HiddenInput())
    folderpk = forms.IntegerField(widget=forms.HiddenInput())
    filepk = forms.IntegerField(widget=forms.HiddenInput())

class deleteSinglesForm(forms.Form):
    action = forms.CharField(max_length=10, initial='deleteSingles', widget=forms.HiddenInput())
    folderpk = forms.IntegerField(widget=forms.HiddenInput())
    filepk = forms.IntegerField(widget=forms.HiddenInput())