from postgresTest.settings import EMAIL_HOST_USER
from django.views.decorators.csrf import csrf_exempt  #to access other domin to access our method
# Create your views here.
from rest_framework.views import APIView
#from postgresTest import testdb
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from testdb.serializer import UserSerializer, RegisterSerializer
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth.models import User
import datetime
from django.core.mail import send_mail
from django.http import HttpResponse


@method_decorator(csrf_exempt, name='dispatch')
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        username = request.data.get('username')
        # email = User.objects.get(username=username).email
        sub="Login Alert"
        timing =datetime.datetime.now().time().strftime("%I:%M %p")
        Message='You have been succesfully loggedin at '+ str(timing) 
        # sendText.mail_bhejde(email,sub,Message)
        return super(LoginAPI, self).post(request, format=None)
    
class sendText():
    def mail_bhejde(email,subject,Message):
        send_mail(subject,Message,EMAIL_HOST_USER,[email,EMAIL_HOST_USER])


class connectAPI(APIView):
    def get(self, request, format=None):
        content={
           'msg': 'angular and Django got married'
        }
        return Response(content)
    def my_view(request):
        response = HttpResponse('Hello, world!')
        response['Access-Control-Allow-Origin'] = '*' # or set to a specific domain
        return response




         