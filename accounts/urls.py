from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm

app_name = 'accounts'

urlpatterns = [
    # path('dashboard/', views.dashboard, name='dashboard'), # 이제 config/urls.py에서 직접 처리하므로 중복입니다.
    path('contents/', views.contents, name='contents'),
    path('contents/add/', views.video_add, name='video_add'),
    path('contents/<int:pk>/update/', views.video_update, name='video_update'),
    path('contents/<int:pk>/delete/', views.video_delete, name='video_delete'),
    path('analysis/', views.analysis, name='analysis'),
    path('monetization/', views.monetization, name='monetization'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        authentication_form=CustomAuthenticationForm # 커스텀 폼을 사용하도록 지정
    ), name='login'),
    # 로그아웃 후 'logged_out.html' 페이지 대신 로그인 페이지로 즉시 리디렉션합니다.
    path('logout/', auth_views.LogoutView.as_view(
        next_page='accounts:login'
    ), name='logout'),
    path('register/', views.register, name='register'),
]