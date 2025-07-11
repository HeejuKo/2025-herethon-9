from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class SignupStep1Form(forms.Form):
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")

        return cleaned_data
    
class SignupStep2Form(forms.Form):
    id_image = forms.ImageField()

class SignupStep4Form(forms.Form):
    nickname = forms.CharField(max_length=10)
    introduction = forms.CharField(max_length=200, widget=forms.Textarea)