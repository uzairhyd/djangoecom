from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactForm #LoginForm, RegisterForm

def home_page(request):
    #print(request.session.get("first_name", "Unkown"))
    context = {
        "title": "Hello World!",
        "content": "Welcome to the homepage.",
    }
    if request.user.is_authenticated:
        context['premium_content'] = "This is premium content."
    return render(request, "home_page.html", context)


def about_page(request):
    context = {
        "title": "About us",
        "content": "Welcome to the about page."
    }
    return render(request, "home_page.html", context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Contact Us",
        "content": "Welcome to the contact us page.",
        "form": contact_form
    }

    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    # if request.method == "POST":
    #     print(request.POST)
    #     print(request.POST.get('fullname'))
    #     print(request.POST.get('email'))
    #     print(request.POST.get('content'))
    return render(request, "contact/view.html", context)


