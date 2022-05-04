from django.urls import path

from .views import SaveRequest, GetUserRequests, DeleteUserRequest

app_name = 'request'
urlpatterns = [
    path('request/save', SaveRequest.as_view()),
    path('request/user', GetUserRequests.as_view()),
    path('request/delete', DeleteUserRequest.as_view()),
]
