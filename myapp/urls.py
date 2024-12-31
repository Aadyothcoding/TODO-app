from django.contrib import admin
from django.urls import path,include
from .import views 

urlpatterns = [
  path('', views.signup, name='signup'),  # Signup page
    path('login/', views.login_view, name='login'),  # Login page
    path('logout/', views.logout_view, name='logout'),  # Logout functionality
    path('home/', views.home_view, name='home'),  # Home page

]