from django import forms

from django.contrib.auth.models import User
from boldpredict.models import *
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password, get_default_password_validators

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20,
                               label = 'Username',
                               required = True,
                               widget = forms.TextInput(attrs={'id' : 'id_username','class' : 'form-control'}),
                               error_messages = {'required':'username cannot be none'},
                               )
    password = forms.CharField(max_length = 20,
                               label = "Password",
                               required = True,
                               widget = forms.PasswordInput(attrs= {'id' : 'id_password','class' : 'form-control'}),
                               error_messages = {'required':'password cannot be none'},
                               )
    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username = username, password = password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        return cleaned_data

class RegistrationForm(forms.Form):
    email = forms.CharField(max_length = 30,
                        label = 'E-mail',
                        required = True,
                        widget = forms.EmailInput(attrs = {'id':'id_email','class' : 'form-control'}),
                        )
    username = forms.CharField(max_length = 20,
                               label = 'Username',
                               required = True,
                               widget = forms.TextInput(attrs={'id' : 'id_username','class' : 'form-control'}),
                               error_messages = {'required':'username cannot be none'},
                               )
    password = forms.CharField(max_length = 20,
                               label = "Password",
                               required = True,
                               widget = forms.PasswordInput(attrs= {'id' : 'id_password','class' : 'form-control'}),
                               error_messages = {'required':'password cannot be none'},
                               )
    confirm_pwd = forms.CharField(max_length = 20,
                                  label = 'Confirm password',
                                  required = True,
                                  widget = forms.PasswordInput(attrs= {'id':'id_confirm_password','class' : 'form-control'}),
                                  error_messages = {'required':'password cannot be none'},
                                  )

    first_name = forms.CharField(max_length = 20,
                                 label = 'First Name',
                                 required = True,
                                 widget = forms.TextInput(attrs = {'id' : 'id_first_name','class' : 'form-control'}),
                                 error_messages = {'required':'first name cannot be none'},
                                 )
    last_name = forms.CharField(max_length = 20,
                                label = 'Last Name',
                                required = True,
                                widget = forms.TextInput(attrs = {'id' : 'id_last_name','class' : 'form-control'}),
                                error_messages = {'required':'last name cannot be none'},
                                )

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        password = cleaned_data.get('password')
        confirm_pwd = cleaned_data.get('confirm_pwd')
        if password and confirm_pwd and password != confirm_pwd:
            raise forms.ValidationError("Password and confirm password don't match.")
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        validate_password(password,password_validators = get_default_password_validators())
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already exist.")
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Email is already registered.")

        return cleaned_data
