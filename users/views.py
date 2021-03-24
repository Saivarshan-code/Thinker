from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.views.generic import CreateView,UpdateView
from .models import userprofile
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login,logout,authenticate
from .forms import UserForm,UserProfileForm
from question.models import question
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic import ListView
from question.filters import QuestionFilter,SearchFilter
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


def index(request):
    question_list = question.objects.filter().order_by('-date')
    # categories = (('maths','maths'), ('biology','biology'), ('physics','physics'), ('chemistry','chemistry'), ('history','history'), ('geography','geography'), ('democratic politics','democratic politics'), ('economics','economics'), ('english','english'), ('Computer science','Computer science'), ('Tamil','Tamil'), ('Hindi','Hindi'), ('General','General'))
    question_filter = SearchFilter(request.GET, queryset = question_list)
    return render(request, 'users/home.html', {'filter' : question_filter})



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


def userprofilepage(request,username):
    try:
        username = userprofile.objects.get(user__username=username)
        user_questions = question.objects.filter(username=username).order_by('-date')
        return render(request,'users/user_profile.html',{'questions':user_questions,
                                                         'username':username })
    except:
        raise Http404

class Update_userprofile(UpdateView,LoginRequiredMixin):
    model = userprofile
    fields = ['std','description','show_your_email_to_others']
