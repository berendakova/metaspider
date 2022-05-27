from django.urls import path

from .views import SaveRequest, GetUserRequests, DeleteUserRequest, GetOldData

app_name = 'request'
urlpatterns = [
    path('request/save', SaveRequest.as_view()),
    path('request/user', GetUserRequests.as_view()),
    path('request/delete', DeleteUserRequest.as_view()),
    path('request/old_db', GetUserRequests.as_view()),
    path('request/old_db/metadata', GetOldData.as_view())
]
