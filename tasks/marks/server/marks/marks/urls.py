from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path
from student import views as s_views
from teacher import views as t_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', s_views.index_page, name='index_page'),
    path('logout',auth_views.LogoutView.as_view(),name="logout"),
    path('login',auth_views.LoginView.as_view(), name='login'),
    path('register', s_views.register, name='register'),
    path('marks', s_views.marks, name='marks'),
    path('question', s_views.question, name='question'),
    path('question/<int:question_id>', s_views.inspect_question, name='inspect_question'),
    path('diary', s_views.diary, name='diary'),
    path('api/activate_teacher', t_views.activate_teacher, name='activate_teacher'),
    path('check_question/<int:question_id>', t_views.check_question, name='check_question'),
    path('new_mark', t_views.new_mark, name='new_mark')
]

urlpatterns += staticfiles_urlpatterns()
