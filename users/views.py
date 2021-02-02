from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from .models import userprofile
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login,logout,authenticate
from .forms import UserForm,UserProfileForm
from question.models import question
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    all_questions = question.objects.filter().order_by('-date')
    return render(request,'users/home.html',{'questions':all_questions})

def loggedout(request):
    return render(request,'users/loggingout.html')

@login_required
def loggingin(request):
    return render(request,'users/loggingin.html')

def SignUp(request):
    signed_up = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        user_profile_form = UserProfileForm(data=request.POST)



        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save(commit=False)

            user.set_password(user.password)

            user.save()

            userprofile = user_profile_form.save(commit=False)
            userprofile.user = user
            userprofile.save()
            login(request,userprofile.user)

            signed_up = True

        else:
            print(user_form.errors,user_profile_form.errors)

    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()

    return render(request,'users/signup.html',
                  {'user_form':user_form,
                   'user_profile_form':user_profile_form,
                   'signed_up':signed_up})
