from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from boldpredict.models import *
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password, get_default_password_validators
import re

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

        try:
            user=User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise forms.ValidationError("User does not exist")
        if authenticate(username = username, password = password) == None and user.is_active == True:
            raise forms.ValidationError("Invalid username/password")
        return cleaned_data

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 20,
                               label = 'Username',
                               required = True,
                               widget = forms.TextInput(attrs={'id' : 'id_username','class' : 'form-control'}),
                               error_messages = {'required':'username cannot be none'},
                               )
    email = forms.CharField(max_length = 30,
                    label = 'E-mail',
                    required = True,
                    widget = forms.EmailInput(attrs = {'id':'id_email','class' : 'form-control'}),
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
        if not all([ (x.isdigit() or x.isalpha()) for x in username ]):
            raise forms.ValidationError("Username should be alphanumeric characters.")
        email = self.cleaned_data.get('email')
        if  not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            raise forms.ValidationError("Wrong format email address!")
        validate_password(password,password_validators = get_default_password_validators())
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already exist.")
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Email is already registered.")

        return cleaned_data

class WordListForm(forms.ModelForm):
    class Meta:
        model = Contrast
        fields = ['contrast_title','list1_name', 'list1_text', 'baseline_choice', 'list2_name', 'list2_text', 'permutation_choice']
        widgets = {
            'contrast_title': forms.Textarea(attrs ={'cols':50, 'rows':1}),
            'list1_name': forms.Textarea(attrs ={'cols':50, 'rows':1}),
            'list2_name': forms.Textarea(attrs ={'cols':50, 'rows':1}),
            'list1_text': forms.Textarea(attrs ={'cols':50, 'rows':10}),
            'list2_text': forms.Textarea(attrs ={'cols':50, 'rows':10}),
            # 'privacy_choice':forms.RadioSelect(),
        }
class ForgotForm(forms.Form):
    email = forms.CharField(max_length = 30,
                        label = 'E-mail',
                        required = True,
                        widget = forms.EmailInput(attrs = {'id':'id_email','class' : 'form-control'}),
                        )
    def clean(self):
        cleaned_data = super(ForgotForm,self).clean()
        email = cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError("Email is not registered")
    
        return cleaned_data


class ResetForm(forms.Form):

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

    def clean(self):
        cleaned_data = super(ResetForm, self).clean()
        password = cleaned_data.get('password')
        confirm_pwd = cleaned_data.get('confirm_pwd')
        if password and confirm_pwd and password != confirm_pwd:
            raise forms.ValidationError("Password and confirm password don't match.")
        validate_password(password,password_validators = get_default_password_validators())
        return cleaned_data
