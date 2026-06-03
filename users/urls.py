from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'user'

urlpatterns = [
    path('signup/',views.SignUp,name='signup'),
    path('token/',views.token_send,name='token_send'),
    path('verify/<auth_token>',views.verify,name='verify'),
    path('logout/',views.logout_view,name='logout'),
    path('login/',views.login,name='login'),
    path('loggedout/',views.loggedout,name='loggingout'),
    path('loggingin/',views.loggingin,name='loggingin'),
    path('<str:username>/',views.userprofilepage,name="user_profile_page"),
    path('<int:pk>/update',views.Update_userprofile.as_view(),name='update_userprofile'),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
