from django.urls import path

from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.register, name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('password/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('dashboard/profile/', views.profile_update, name='profile_update'),
]
