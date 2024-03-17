from django.contrib.auth.models import User
from django.contrib.auth import authenticate


def authenticate_user(*,req, username, password) -> User:
    user = authenticate(request=req,username=username, password=password)
    return user
