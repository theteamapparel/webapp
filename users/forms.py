from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import get_user_model
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': '', 'placeholder': 'First Name'}),
        label="First Name*")

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': '', 'placeholder': 'Last Name'}),
        label="Last Name*")

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': '', 'placeholder': 'Username'}),
        label="Username*")
    
    
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': '', 'placeholder': 'Email'}),
        label="Email*",
        help_text='A valid email address, please.', 
        required=True)
    
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'password', 'placeholder': 'Password'}),
        label="Username*")
    
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'password', 'placeholder': 'Confirm Password'}),
        label="Confirm Password*")

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': '', 'placeholder': 'Username or Email'}),
        label="Username or Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'password', 'placeholder': 'Password'}))

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'image', 'description']

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']
    new_password1=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password', 'placeholder': 'Password'}))
    new_password2=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password', 'placeholder': 'Confirm Password'}))

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': '', 'placeholder': 'email'}),
        label="email*")

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())