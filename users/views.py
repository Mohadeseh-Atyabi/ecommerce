from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .login import Login
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .services import authenticate_user
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


class LoginUser(View):
    costumer_page = 'product_customer'
    seller_page = 'product_seller'
    login_template = 'login.html'

    def get(self, req):
        if req.user.is_anonymous:
            form = Login()
            return render(req, self.login_template, {'form': form})
        else:
            return self.redirect_portal(req.user)

    def post(self, req):
        form = Login(req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate_user(req=req, username=username, password=password)
            if user:
                login(req, user)
                return self.redirect_portal(user)
            else:
                messages.error(req, 'User not found. Try again!')
                return render(req, self.login_template, {'form': form})

    def redirect_portal(self, user):
        if user.groups.filter(name='seller').exists():
            print("seller")
            return redirect(self.seller_page)
        elif user.groups.filter(name='customer').exists():
            print('costumer')
            return redirect(self.costumer_page)


class LogoutUser(View):
    template = 'login'

    @method_decorator(login_required)
    def get(self, req):
        logout(req)
        return redirect(self.template)


# class LoginUserAPI(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, req):
#         username = req.data.get('username')
#         password = req.data.get('password')
#         user = authenticate_user(username=username, password=password)
#         payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#         encode_handler = api_settings.JWT_ENCODE_HANDLER
#         payload = payload_handler(user)
#         token = encode_handler(payload)
#         return JsonResponse({
#             'token': token
#         })

class User(APIView):
    @extend_schema(
        responses=UserSerializer,
    )
    def get(self, req):
        serializer = UserSerializer(req.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
