from django.db import models
from users.models import userprofile


# Create your models here.
class question(models.Model):
    username = models.ForeignKey(userprofile,blank=True,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=150,help_text='*required')
    description = models.CharField(max_length=150,null=True,help_text='*required')
    date = models.DateTimeField(auto_now_add=True)
    categories = (('maths','maths'),('biology','biology'),('physics','physics'),('chemistry','chemistry'),('history','history'),('geography','geography'),('democratic politics','democratic politics'),('economics','economics'),('english','english'),
                  ('Computer science','Computer science'),('Tamil','Tamil'),('Hindi','Hindi'),('General','General'))
    category = models.CharField(max_length=100,choices=categories,default='maths',help_text='*required')
    image1 = models.ImageField(upload_to="question/images/",blank=True,null=True)
    image2 = models.ImageField(upload_to="question/images/",blank=True,null=True)
    image3 = models.ImageField(upload_to="question/images/",blank=True,null=True)
    file = models.FileField(upload_to='question/files/',blank=True)
    question = models.TextField(max_length=None,help_text='*required')
    upvote = models.ManyToManyField(userprofile,blank=True,related_name="upvoted_question")
    # downvote = models.ManyToManyField(userprofile,blank=True,default=0,related_name="downvote")
    views = models.PositiveIntegerField(default=0)
    user_viewed =  models.ManyToManyField(userprofile,blank=True,related_name="viewd_question")
    reported_users = models.ManyToManyField(userprofile,blank=True,related_name="report_question")
    report = models.PositiveIntegerField(default=0)
    bookmark_question = models.ManyToManyField(userprofile,blank=True,related_name="bookmark_question")



    def __str__(self):
        return self.title

class comment(models.Model):
    related_question = models.ForeignKey(question,on_delete=models.CASCADE,related_name='comments',blank=True,null=True)
    username = models.ForeignKey(userprofile,blank=True,on_delete=models.CASCADE,null=True)
    comment_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    time = models.TimeField(auto_now=True)
    image1 = models.ImageField(upload_to="comment/images/",blank=True,null=True)
    image2 = models.ImageField(upload_to="comment/images/",blank=True,null=True)
    file = models.FileField(upload_to='comment/files/',blank=True)
    comment = models.TextField(max_length=1000000)
    upvote_comment = models.ManyToManyField(userprofile,blank=True,related_name="upvoted_comment")
    downvote_comment = models.ManyToManyField(userprofile,blank=True,related_name="downvote_comment")
    comment_votes = models.IntegerField(blank=True,null=True,default=0)
    reported_users = models.ManyToManyField(userprofile,blank=True,related_name="report_comment")
    report = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.comment
