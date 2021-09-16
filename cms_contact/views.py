from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from cms_settings.models import SiteSetting
from .models import ContactUs, NewsletterSignUp
from .forms import CreateContactForm, NewsletterSignupForm


# Create your views here.


def contact_page(request):
    contact_form = CreateContactForm(request.POST or None)

    if contact_form.is_valid():
        full_name = contact_form.cleaned_data.get('full_name')
        email = contact_form.cleaned_data.get('email')
        subject = contact_form.cleaned_data.get('subject')
        text = contact_form.cleaned_data.get('text')
        ContactUs.objects.create(full_name=full_name, email=email, subject=subject, text=text, is_read=False)
        # todo : show user a success message
        contact_form = CreateContactForm()

    setting = SiteSetting.objects.first()

    context = {
        'contact_form': contact_form,
        'setting': setting
    }

    return render(request, 'contact_us_page.html', context)


def newsletter_signup(request, *args, **kwargs):
    newsletter_signup_form = NewsletterSignupForm(request.POST or None)

    if newsletter_signup_form.is_valid():
        full_name = newsletter_signup_form.cleaned_data.get('full_name')
        email = newsletter_signup_form.cleaned_data.get('email')
        NewsletterSignUp.objects.create(full_name=full_name, email=email)
        newsletter_signup_form = NewsletterSignupForm()

    context = {
        'newsletter_form': newsletter_signup_form,
    }

    return render(request, 'newsletter_signup.html', context)
