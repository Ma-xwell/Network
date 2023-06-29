from django import forms

class NewPostForm(forms.Form):
    text = forms.CharField(max_length=250, widget=forms.Textarea)
