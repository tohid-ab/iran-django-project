from django import forms
from django.contrib.auth.models import User
from django.forms import Textarea, FileInput, TextInput
from .models import Profile


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("پسورد اشتباه است"))
        except User.DoesNotExist:
            self.add_error("username", forms.ValidationError("کاربر وجود ندارد"))
        return super().clean()


class UserRegistrationForm(forms.ModelForm):
    email = forms.CharField(required=True)
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']