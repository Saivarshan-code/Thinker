from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .forms import questionform,YourForm,CommentForm
from .models import question,comment
from users.models import userprofile
from django.template import Context
from django.http import HttpResponseRedirect
from django.urls import reverse
from question.filters import QuestionFilter
from django.views.generic import ListView

# Create your views here.

@login_required
def new_question(request):
    form = YourForm()

    if request.method == 'POST':
        form = YourForm(request.POST,request.FILES)
        username = userprofile.objects.get(user=request.user)
        if form.is_valid():
            questions = form.save(commit=False)
            questions.username = username
            questions.save()
            return redirect('question:myquestions')
        else:
            return render(request,'question/question.html',{'error':form.errors})
    else:
        return render(request, 'question/question.html',{'question':form})


def viewquestion(request,question_pk):
    detailed_question = get_object_or_404(question, pk=question_pk)
    try:
        username = userprofile.objects.get(user=request.user)
        if username not in detailed_question.user_viewed.all():
            detailed_question.user_viewed.add(username)
            detailed_question.views += 1
    except:
        nothing = True

    try:
        comments = comment.objects.filter(related_question=detailed_question).order_by('-comment_votes')
    except:
        comments = 0

    if detailed_question.report*4 > detailed_question.views and detailed_question.report > 10:
        detailed_question.delete()
        return redirect('index')


    if str(request.user) == str(detailed_question.username):
        update_and_delete = 100
        return render(request,'question/view_question.html',
                      {'question':detailed_question,
                       'update_and_delete': 100,
                       'comments':comments})
    else:
        update_and_delete = 10
        return render(request,'question/view_question.html',{'question':detailed_question,
                                                             'update_and_delete': 10,
                                                             'comments':comments })



@login_required
def updatequestion(request,question_pk):
    detailed_question = get_object_or_404(question, pk=question_pk)
    form = YourForm(instance=detailed_question)

    if request.method == 'POST':
        form = questionform(request.POST,instance=detailed_question)
        form.save()
        return redirect('question:myquestions')
    return render(request,'question/update_question.html',{'question':detailed_question,'form':form})

@login_required
def deletequestion(request,question_pk):
    questions = get_object_or_404(question, pk=question_pk)
    detailed_question = get_object_or_404(question,pk=question_pk)
    if request.method == 'POST':
        detailed_question.delete()
        return redirect('index')

    return render(request,'question/confirm_delete.html',{'question':questions})


@login_required
def new_comment(request,question_pk):
    if request.method == 'POST':
        form = CommentForm(request.POST,request.FILES)
        username = userprofile.objects.get(user=request.user)
        detailed_question = get_object_or_404(question, pk=question_pk)

        try:
            comments = comment.objects.get(related_question=detailed_question)
        except:
            comments = "Be the first to answer!"
        if form.is_valid():
            comment_store = form.save(commit=False)
            comment_store.username = username
            comment_store.related_question = detailed_question
            comment_store.save()
            return redirect('index')
        else:
            return render(request,'question/comment.html',{'error':form.errors})
    else:
        try:
            comment_question = get_object_or_404(question,pk=question_pk)
        except:
            pass
        form = CommentForm()
        return render(request,'question/comment.html',
                       {'form':form,'question_pk':question_pk})

@login_required
def upvote(request,question_pk):
    # if request.method == 'POST':
    detailed_question = get_object_or_404(question, pk=question_pk)
    username = userprofile.objects.get(user=request.user)
    if username in detailed_question.upvote.all():
        detailed_question.upvote.remove(username)
    else:
        detailed_question.upvote.add(username)
    return HttpResponseRedirect(reverse('question:viewquestion',args=[question_pk]))

@login_required
def report_question(request,question_pk):
    detailed_question = get_object_or_404(question, pk=question_pk)
    username = userprofile.objects.get(user=request.user)
    if username in detailed_question.reported_users.all():
        detailed_question.reported_users.remove(username)
        detailed_question.save()
    else:
        detailed_question.reported_users.add(username)
        detailed_question.report += 1
        detailed_question.save()
    return HttpResponseRedirect(reverse('question:viewquestion',args=[question_pk]))


@login_required
def upvote_comment(request,question_pk,comment_pk):
    detailed_question = get_object_or_404(question, pk=question_pk)
    comment_object = get_object_or_404(comment,pk=comment_pk,related_question=detailed_question)
    username = userprofile.objects.get(user=request.user)
    if username in comment_object.upvote_comment.all():
        comment_object.upvote_comment.remove(username)
        comment_object.comment_votes -= 1
        comment_object.save()
    else:
        comment_object.upvote_comment.add(username)
        comment_object.comment_votes += 1
        comment_object.save()
    return HttpResponseRedirect(reverse('question:viewquestion',args=[question_pk]))

@login_required
def downvote_comment(request,question_pk,comment_pk):
    detailed_question = get_object_or_404(question, pk=question_pk)
    comment_object = get_object_or_404(comment,pk=comment_pk,related_question=detailed_question)
    username = userprofile.objects.get(user=request.user)
    if username in comment_object.downvote_comment.all():
        comment_object.downvote_comment.remove(username)
        comment_object.comment_votes += 1
        comment_object.save()
    else:
        comment_object.downvote_comment.add(username)
        comment_object.comment_votes -= 1
        comment_object.save()
    return HttpResponseRedirect(reverse('question:viewquestion',args=[question_pk]))

@login_required
def report_comment(request,question_pk,comment_pk):
    detailed_question = get_object_or_404(question,pk=question_pk)
    comment_object = get_object_or_404(comment,pk=comment_pk,related_question=detailed_question)
    username = userprofile.objects.get(user=request.user)
    if username in comment_object.reported_users.all():
        comment_object.reported_users.remove(username)
        comment_object.save()
    else:
        comment_object.reported_users.add(username)
        comment_object.report+=1
        if comment_object.report*6 > detailed_question.views and comment_object.report>=3:
            comment_object.delete()
        else:
            comment_object.save()
    return HttpResponseRedirect(reverse('question:viewquestion',args=[question_pk]))

def myquestions(request):
    try:
        username = userprofile.objects.get(user=request.user)
    except:
        pass
    if request.user.is_authenticated:
        my_questions = question.objects.filter(username=username).order_by('-upvote')

        return render(request,'question/myquestions.html',{'questions':my_questions,
                                                         'username':username })
    else:
        return render(request,'question/myquestions.html')


def question_list(request):
    question_list = question.objects.all()
    # categories = (('maths','maths'), ('biology','biology'), ('physics','physics'), ('chemistry','chemistry'), ('history','history'), ('geography','geography'), ('democratic politics','democratic politics'), ('economics','economics'), ('english','english'), ('Computer science','Computer science'), ('Tamil','Tamil'), ('Hindi','Hindi'), ('General','General'))
    question_filter = QuestionFilter(request.GET, queryset = question_list)
    return render(request, 'question/filter_questions.html', {'filter' : question_filter})
