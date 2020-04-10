from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from accounts import views
from django.contrib.auth.decorators import login_required
from accounts.views import UpdateUser
app_name = 'accounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='user_login'),
    path('sign-up/', views.register, name='sign-up'),
    path('users/', views.user_list, name="userprofileinfo_list"),
    path('users/<int:pk>/change-avatar', views.change_avatar, name="update_avatar"),
    path('users/<int:pk>', views.user_detail, name="userprofileinfo_detail"),
    path('users/<int:pk>/edit-profile', UpdateUser.as_view(), name="userprofileinfo_update"),
]
