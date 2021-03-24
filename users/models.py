from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class userprofile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    choices = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),('11','11'),('12','12'),('College','College'),('work','work'))
    show_your_email_to_others = models.BooleanField(default=False)
    std = models.CharField(max_length=7,choices= choices,help_text='Required')
    description = models.TextField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.user.username
