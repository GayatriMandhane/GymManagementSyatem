from django.views.decorators.csrf import csrf_exempt  #to access other domin to access our method
from rest_framework.parsers import JSONParser  #incoming data into data model
from django.http.response import JsonResponse  
from testdb.serializer import enquirySerializer
from testdb.models import enquiry


@csrf_exempt
def enquiryApi(request,id=0):
   if request.method == 'GET':
      enq = enquiry.objects.all()
      enq_ser = enquirySerializer(enq,many=True)  #using serializer class to convert it to json
      return JsonResponse(enq_ser.data,safe=False)
   elif request.method == 'POST':
      enq_data = JSONParser().parse(request)  #passing request and using serilizer to convert it into model
      enq_ser = enquirySerializer(data=enq_data)
      print(enq_ser)
      if enq_ser.is_valid():
         enq_ser.save()
         return JsonResponse("Added successfully",safe=False)
      return JsonResponse("Failed to Add",safe=False)
   elif request.method == 'PUT':
      enq_data = JSONParser().parse(request) #1st capturing exciting record
      enq = enquiry.objects.get(eId = enq_data['eId'])
      enq_ser = enquirySerializer(enq,data=enq_data)
#mapping it with new values using serializers class
      if enq_ser.is_valid():
         enq_ser.save()
         return JsonResponse("Update Successfully",safe=False)
      return JsonResponse("Failed to Update")
   elif request.method == 'DELETE':
      x=slice(9,len(request.path))
      enq_data = request.path[x]
      print(enq_data)
      enq_data = int(enq_data)
      if(enquiry.objects.filter(eId=enq_data)):
         enq = enquiry.objects.get(eId=enq_data)
         enq.delete()
         return JsonResponse("Deleted Successfully",safe=False) 
      return JsonResponse("Enquiry Id does not exist!",safe=False)
      




         