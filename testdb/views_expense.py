from django.views.decorators.csrf import csrf_exempt  #to access other domin to access our method
from rest_framework.parsers import JSONParser  #incoming data into data model
from django.http.response import JsonResponse  
# Create your views here.
from testdb.serializer import expenseSerializer
from testdb.models import expense


@csrf_exempt
def expenseApi(request,id=0):
   if request.method == 'GET':
      exp = expense.objects.all()
      exp_ser = expenseSerializer(exp,many=True)  #using serializer class to convert it to json
      return JsonResponse(exp_ser.data,safe=False)
   elif request.method == 'POST':
      exp_data = JSONParser().parse(request)  #passing request and using serilizer to convert it into model
      exp_ser = expenseSerializer(data=exp_data)
      print(exp_ser)
      if exp_ser.is_valid():
         exp_ser.save()
         return JsonResponse("Added successfully",safe=False)
      return JsonResponse("Failed to Add",safe=False)




         