from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.index, name="home"),
    path('login/', views.loginuser, name="login"),
    path('logout/', views.logoutuser, name="logout"),
    path('register/', views.register, name="register"),
    path('deluser/', views.deluser, name="deluser"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('profile/', views.profile, name="profile"),
    path('authorprofile/', views.authorprofile, name="authorprofile"),
    path('deluser/', views.deluser, name="deluser"),
    path('about/', views.about, name="about"),
    path('bookmarked/', views.bookmarked, name="bookmarked"),
    path('marked/', views.marked, name="bookmarked"),
    path('myblogs/', views.myblogs, name="myblogs"),
    path('blogs/', views.blogs, name="blogs"),
    path('blogs/<id>/', views.blogs, name="blogs"),
    # path('blogs/', views.blogs, name="blogs"),
    path('upload/', views.upload, name="upload"),
    path('mdtohtml/', views.mdtohtml, name="mdtohtml"),


]
