from rest_framework.views import APIView


#Пользователь отправляет запрос на определнный паук
class SendResponse(APIView):
    def post(self):
        return 1
