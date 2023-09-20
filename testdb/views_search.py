from rest_framework.generics import  ListAPIView
from testdb.serializer import membersSerializer, subscriptionSerializer,attendenceSerializer
from .models import  attendence, members, subscription 
from rest_framework.filters import SearchFilter


class MemberSearch(ListAPIView):
    queryset = members.objects.all()
    serializer_class= membersSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name','=memberid']

class AttendanceSearch(ListAPIView):
    queryset = attendence.objects.all()
    serializer_class= attendenceSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

class BillSearch(ListAPIView):
    queryset = subscription.objects.all()
    serializer_class= subscriptionSerializer
    filter_backends = [SearchFilter]
    search_fields = ['^name']


