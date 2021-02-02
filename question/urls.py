from . import views
from django.urls import path
from django.conf import settings
# from django.contrib.staticfiles.urls import static
from django.conf.urls.static import static
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns





app_name = 'question'

urlpatterns = [
    path('new_question/',views.new_question,name='new_question'),
    path('viewquestion/<int:question_pk>/',views.viewquestion,name="viewquestion"),
    path('update_question/<int:question_pk>/',views.updatequestion,name="update_question"),
    path('delete_question/<int:question_pk>/',views.deletequestion,name="delete_question"),
    path('new_comment/<int:question_pk>/',views.new_comment,name='new_comment'),
    path('viewquestion/<int:question_pk>/upvote/',views.upvote,name="upvote"),
    path('viewquestion/<int:question_pk>/report/',views.report_question,name="report"),
    path('viewquestion/<int:question_pk>/<int:comment_pk>/upvote_comment/',views.upvote_comment,name="upvote_comment"),
    path('viewquestion/<int:question_pk>/<int:comment_pk>/downvote_comment/',views.downvote_comment,name="downvote_comment"),
    path('viewquestion/<int:question_pk>/<int:comment_pk>/report_comment/',views.report_comment,name="report_comment"),
    path('myquestions/',views.myquestions,name="myquestions"),
    # path('viewquestion/<int:question_pk>/bookmark_question/',views.bookmark_question,name="bookmark_question"),
    # path('bookmarked_question/',views.bookmarked_question,name="bookmarked_questions"),
    ]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
