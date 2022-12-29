from django import forms
from . import models
from django.core.validators import RegexValidator


class SearchRoom(forms.Form):
    checkin_date = forms.DateField()
    checkout_date = forms.DateField()
    category_id = forms.IntegerField()

phone_validator = RegexValidator(
    r"((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))", "Your phone number should be (xxx)xxxxxxxxx or 0xxxxxxxxx")

class FormContact(forms.ModelForm):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
                           'class': 'form-control fh5co_contact_text_box'}))
    phone= forms.CharField(max_length=20, validators=[phone_validator], widget=forms.TextInput(
        attrs={
               'class': 'form-control fh5co_contact_text_box',
               'pattern': '((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))',
               'title': 'Your phone number should be (xxx)xxxxxxxxx or 0xxxxxxxxx'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(
        attrs={'class': 'form-control fh5co_contact_text_box'}))
    subject = forms.CharField(label='Subject', widget=forms.TextInput(
        attrs={'class': 'form-control fh5co_contact_text_box'}))
    message = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control fh5co_contacts_message'}))

    class Meta:
        model = models.Contact
        fields = '__all__'

class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=150, widget=forms.PasswordInput())
    confirm = forms.CharField(max_length=150, widget=forms.PasswordInput())   

    class Meta():
        model = models.User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class UserProfileInfoForm(forms.ModelForm):
    phone = forms.CharField(max_length=20, validators=[phone_validator])

    class Meta():
        model = models.UserProfileInfo
        exclude = ('user', )
