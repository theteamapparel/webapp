from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import ProductReview,UserAddressBook

class SignupForm(UserCreationForm):
	class Meta:
		model=User
		fields=('first_name','last_name','email','username','password1','password2')

# Review Add Form
class ReviewAdd(forms.ModelForm):
	class Meta:
		model=ProductReview
		fields=('review_text','review_rating')

# AddressBook Add Form
class AddressBookForm(forms.ModelForm):
	class Meta:
		model=UserAddressBook
		fields=('address_name','country','town_or_city','address','postal_code','mobile','status')

# ProfileEdit
class ProfileForm(UserChangeForm):
	class Meta:
		model=User
		fields=('first_name','last_name','email','username')


# Contact Form
class ContactForm(forms.Form):
	name = forms.CharField(widget=forms.TextInput(
        attrs={'class': '', 'placeholder': 'Name'}),
        label="Name*")
	email_address = forms.CharField(widget=forms.TextInput(
        attrs={'class': '', 'placeholder': 'Email'}),
        label="Email*")
	message = forms.CharField(widget = forms.Textarea(
		attrs={'class': '', 'placeholder': 'Message'}),
		label="Message*")