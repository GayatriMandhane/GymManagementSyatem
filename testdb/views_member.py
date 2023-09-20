import datetime
from django.views.decorators.csrf import csrf_exempt #to access other domin to access our method
from rest_framework.parsers import JSONParser  # incoming data into data model
from django.http.response import JsonResponse
from testdb.models import subscription
from testdb.views import sendText
from testdb.serializer import membersSerializer
from testdb.models import members


@csrf_exempt
def membersApi(request,id=0):
   if request.method == 'GET':
      # mem = members.objects.all()
      dash_all=members.objects.all()
      dash_staff=members.objects.filter(role="staff").values()
      dash_member=members.objects.filter(role="member").values()
      dash_trainee = members.objects.filter(role="trainee").values()
      all_ser = membersSerializer(dash_all,many=True) 
      staff_ser = membersSerializer(dash_staff,many=True)
      member_ser= membersSerializer(dash_member,many=True) 
      trainee_ser=membersSerializer(dash_trainee,many=True)
      subscription_data = subscription.objects.all().values('memberid','endPlanDate')
      dateVal=[]
      for i in range(0,len(all_ser.data)):
         dateVal=[]
         for j in range(0,len(subscription_data)):
            if all_ser.data[i]['memberid']==subscription_data[j]['memberid']:
               dateVal.append(subscription_data[j]['endPlanDate'])
         # print(i,j)
         if dateVal:
            print(max(dateVal))
            latest_date=max(dateVal)
            all_ser.data[i]['endPlanDate']=latest_date
         else:
            all_ser.data[i]['endPlanDate']='No Data'

      for i in range(0,len(member_ser.data)):
         dateVal=[]
         for j in range(0,len(subscription_data)):
            if member_ser.data[i]['memberid']==subscription_data[j]['memberid']:
               dateVal.append(subscription_data[j]['endPlanDate'])
         # print(i,j)
         if dateVal:
            print(max(dateVal))
            latest_date=max(dateVal)
            member_ser.data[i]['endPlanDate']=latest_date
         else:
            member_ser.data[i]['endPlanDate']='No Data'
            

      return JsonResponse({"all":all_ser.data, "staff":staff_ser.data,"member":member_ser.data,
      "trainee":trainee_ser.data},safe=False)
   elif request.method == 'POST':
      mem_data = JSONParser().parse(request)  #passing request and using serilizer to convert it into model
      # email = mem_data['email']
      if(mem_data['email']==''):
         mem_data['email']=None
      if(mem_data['altphone']==''):
         mem_data['altphone']=None
      print(mem_data)
      mem_ser = membersSerializer(data=mem_data)
      # email = mem_data['email']
      name = mem_data['name']
      sub="Member Registration Alert"
      timing =datetime.datetime.now().time().strftime("%I:%M %p")
      message= "Welcome to Power Up Women's Gym "+name+'. You have been succesfully registered at '+ str(timing) 
      if mem_ser.is_valid():
         mem_ser.save()
         # sendText.mail_bhejde(email,sub,message)
         return JsonResponse(mem_ser.data ,safe=False) #"Added successfully",
      return JsonResponse("Failed to Add",safe=False)
   elif request.method == 'PUT':
      mem_data = JSONParser().parse(request) #1st capturing exciting record
      mem = members.objects.get(memberid = mem_data['memberid'])
      mem_ser = membersSerializer(mem,data=mem_data)

#mapping it with new values using serializers class
      if mem_ser.is_valid():
         mem_ser.save()
         return JsonResponse("Update Successfully",safe=False)
      return JsonResponse("Failed to Update")
   elif request.method == 'DELETE':
      x=slice(9,len(request.path))
      mem_data = request.path[x]
      mem_data = int(mem_data)
      if(members.objects.filter(memberid=mem_data)):
         mem = members.objects.get(memberid=mem_data)
         mem.delete()
         return JsonResponse("Deleted Successfully",safe=False) 
      return JsonResponse("Member Id does not exist!",safe=False)

