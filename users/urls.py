from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name="login"),
    path('logout/', views.LogoutUser.as_view(), name="logout"),
    path('user/', views.User.as_view(), name="user")
]
