from django.urls import path

from .views import LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView

app_name = 'authentication'
urlpatterns = [
    path('users', RegistrationAPIView.as_view()),
    path('users/login', LoginAPIView.as_view()),
    path('users/', UserRetrieveUpdateAPIView.as_view()),
]