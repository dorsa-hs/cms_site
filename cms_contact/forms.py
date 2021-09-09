from django import forms
from .models import ContactUs
from django.core import validators


class CreateContactForm(forms.ModelForm):
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'لطفا نام و نام خانوادگی خود را وارد نمایید', 'class': 'form-control'}),
        label='نام و نام خانوادگی',
        validators=[
            validators.MaxLengthValidator(150, 'نام و نام خانوادگی شما نمیتواند بیشتر از 150 کاراکتر باشد')
        ]
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'لطفا ایمیل خود را وارد نمایید', 'class': 'form-control'}),
        label='ایمیل',
        validators=[
            validators.MaxLengthValidator(100, 'ایمیل شما نمیتواند بیشتر از 100 کاراکتر باشد')
        ]
    )

    subject = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا عنوان خود را وارد نمایید', 'class': 'form-control'}),
        label='عنوان',
        validators=[
            validators.MaxLengthValidator(200, 'عنوان پیام شما نمیتواند بیشتر از 200 کاراکتر باشد')
        ]
    )

    class Meta:
        model = ContactUs
        fields = (
            'full_name',
            'email',
            'subject',
            'text'
        )
