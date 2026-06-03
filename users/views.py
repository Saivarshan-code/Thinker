from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import userprofile
from django.contrib.auth import login as auth_login
from .forms import UserForm,UserProfileForm
from question.models import question
from django.contrib.auth.decorators import login_required
from django.conf import settings
from question.filters import QuestionFilter,SearchFilter
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.http import Http404
import uuid
from django.contrib.auth import authenticate




# Create your views here.


def index(request):
    question_list = question.objects.filter().order_by('-date')
    # categories = (('maths','maths'), ('biology','biology'), ('physics','physics'), ('chemistry','chemistry'), ('history','history'), ('geography','geography'), ('democratic politics','democratic politics'), ('economics','economics'), ('english','english'), ('Computer science','Computer science'), ('Tamil','Tamil'), ('Hindi','Hindi'), ('General','General'))
    question_filter = SearchFilter(request.GET, queryset = question_list)
    return render(request, 'users/home.html', {'filter' : question_filter})


# class index(ListView):
#     paginate_by = 5
#     template_name = 'users/home.html'
#
#     def get_queryset(self):
#         self.question_list = question.objects.filter().order_by('-date')
#         self.SearchFilter = SearchFilter(self.request.GET, queryset = self.question_list)
#         return self.SearchFilter


def loggedout(request):
    return render(request,'users/loggingout.html')

@login_required
def loggingin(request):
    return render(request,'users/loggingin.html')

def SignUp(request):
    signed_up = False

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        std = request.POST.get('std')

        user_form = UserForm(data=request.POST)
        user_profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():

            if User.objects.filter(username=username).first():
                messages.success(request,'Username is already taken')
                return redirect('user:signup')

            if User.objects.filter(email=email).first():
                messages.success(request,'Email is already taken. If you are the one who already registered and trying to register again. Check in the mail from saivarshankr@gmail.com, verify your email and login in the link given in the mail')
                return redirect('user:signup')

            user_obj = User(username = username,email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())

            profile_obj, created = userprofile.objects.get_or_create(user = user_obj)
            profile_obj.std = std
            profile_obj.auth_token = auth_token
            profile_obj.save()
            signed_up = True
            send_mail_after_registration(email,auth_token)
            return redirect('user:token_send')


    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()

    return render(request,'users/signup.html',
                  {'user_form':user_form,
                   'user_profile_form':user_profile_form,
                   'signed_up':signed_up})

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/user/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()

        if user_obj is None:
            messages.success(request,'Username not found!')
            return redirect('user:login')

        profile_obj = userprofile.objects.filter(user=user_obj).first()

        if not profile_obj.is_verified:
            messages.success(request,'Your account is not verefied. Check your mail')
            return redirect('user:login')
        user = authenticate(username=username,password=password)
        if user is None:
            messages.success(request,'Wrong password')
            return redirect('user:login')
        auth_login(request,user)
        return redirect('/')

    return render(request,'users/login.html')

def verify(request,auth_token):
    try:
        profile_obj = userprofile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request,'Your account have already been verified!')
                return redirect('user:login')

            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request,'Congratulations your account have been verified!')
            return redirect('user:login')
        else:
            return Http404
    except Exception as e:
        print(e)

def token_send(request):
    if not User.is_authenticated or not User.is_superuser:
        return Http404
    return render(request,'users/token_send.html')

def userprofilepage(request,username):
    try:
        username = userprofile.objects.get(user__username=username)
        user_questions = question.objects.filter(username=username).order_by('-date')
        return render(request,'users/user_profile.html',{'questions':user_questions,
                                                         'username':username })
    except:
        raise Http404

class Update_userprofile(UpdateView,LoginRequiredMixin):
    fields = ('std','description','showing_email')
    model = userprofile


from django.contrib.auth import logout as auth_logout

def logout_view(request):
    auth_logout(request)
    return redirect('user:loggingout')

