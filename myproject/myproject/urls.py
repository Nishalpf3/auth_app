"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin/',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('',views.HomePage,name='home'),
    path('logout/',views.LogoutPage,name='logout'),
    path('admin_login/',views.AdminPage,name='admin_login'),
    #path('adminn/',views.admin_login,name='adminn'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('users/', views.users, name='users'),
    path('insert/', views.user_insert, name='insert'),
    path('<int:id>/', views.user_insert, name='update'),
    path('delete/<int:id>/', views.user_delete, name='delete'),
    path('search/', views.search, name='search')
]

