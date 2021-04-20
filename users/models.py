from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class userprofile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    choices = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),('11','11'),('12','12'),('College','College'),('work','work'))
    showing_email = models.BooleanField(default=False,verbose_name="Show your Email to others:")
    std = models.CharField(max_length=7,choices= choices,help_text='Required')
    description = models.TextField(max_length=255,blank=True,null=True)
    auth_token = models.CharField(max_length=100,default='e8372d63-c78c-45e7-97e1-6c31d6e5ce35')

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("user:user_profile_page",kwargs={'username':self.user.username})
