from asyncio.windows_events import NULL
import datetime
from select import select
from unicodedata import name
from django.shortcuts import render
from rest_framework import status 
from django.views.decorators.csrf import csrf_exempt  #to access other domin to access our method
from rest_framework.parsers import JSONParser  #incoming data into data model
from django.http.response import JsonResponse  
from rest_framework.decorators import api_view

from testdb.serializer import attendenceSerializer
from testdb.models import attendence ,subscription,members


# Create your views here.

@csrf_exempt
def attendenceApi(request,id=0):
   if request.method == 'GET':
      atten = attendence.objects.all()
      atten_m = attendence.objects.filter(role="member").values()
      atten_t = attendence.objects.filter(role="trainee").values()
      atten_s = attendence.objects.filter(role="staff").values()      
      atten_ser = attendenceSerializer(atten,many=True)
      atten_m_ser= attendenceSerializer(atten_m,many=True)  
      atten_t_ser= attendenceSerializer(atten_t,many=True)
      atten_s_ser= attendenceSerializer(atten_s,many=True)
      subscription_data = subscription.objects.all().values('memberid','endPlanDate')
      dateVal=[]
      for i in range(0,len(atten_ser.data)):
         dateVal=[]
         for j in range(0,len(subscription_data)):
            if atten_ser.data[i]['memberid']==subscription_data[j]['memberid']:
               dateVal.append(subscription_data[j]['endPlanDate'])
         # print(i,j)
         if dateVal:
            print(max(dateVal))
            latest_date=max(dateVal)
            atten_ser.data[i]['endPlanDate']=latest_date
         else:
            atten_ser.data[i]['endPlanDate']='No Data'
            
      for i in range(0,len(atten_m_ser.data)):
         dateVal=[]
         for j in range(0,len(subscription_data)):
            if atten_m_ser.data[i]['memberid']==subscription_data[j]['memberid']:
               dateVal.append(subscription_data[j]['endPlanDate'])
         # print(i,j)
         if dateVal:
            print(max(dateVal))
            latest_date=max(dateVal)
            atten_m_ser.data[i]['endPlanDate']=latest_date
         else:
            atten_m_ser.data[i]['endPlanDate']='No Data'
      
      return JsonResponse({"all":atten_ser.data,"member":atten_m_ser.data,
      "trainee":atten_t_ser.data,"staff":atten_s_ser.data},safe=False)
   if request.method == 'POST':
      mem_id = JSONParser().parse(request)  #passing request and using serilizer to convert it into model
      if (members.objects.filter(memberid=mem_id["memberid"])):
            att=members.objects.filter(memberid=mem_id["memberid"]).values()
            attVal={}
            todays_data = attendence.objects.filter(memberid=mem_id["memberid"], date=datetime.date.today()).values()
            if (todays_data.count()==0):
               for i in att:
                  attVal["memberid"]=i["memberid"]
                  attVal["date"]=datetime.date.today()
                  attVal["timeout"]="None"
                  attVal["timein"]=str(datetime.datetime.now().time().strftime("%I:%M %p"))
                  attVal["name"]=i["name"]
                  attVal["role"]=i["role"]
                  print("odd")
            elif (todays_data.count()==1):
               for i in att:
                     attVal["memberid"]=i["memberid"]
                     attVal["date"]=datetime.date.today()
                     attVal["timein"]="None"
                     attVal["timeout"]=str(datetime.datetime.now().time().strftime("%I:%M %p"))
                     attVal["name"]=i["name"]
                     attVal["role"]=i["role"]
                     print("even")
            else:
               if (todays_data.count() % 2 == 0):
                  for i in att:
                     attVal["memberid"]=i["memberid"]
                     attVal["date"]=datetime.date.today()
                     attVal["timeout"]="None"
                     attVal["timein"]=str(datetime.datetime.now().time().strftime("%I:%M %p"))
                     attVal["name"]=i["name"]
                     attVal["role"]=i["role"]
                     print("odd")
               else:
                  for i in att:
                     attVal["memberid"]=i["memberid"]
                     attVal["date"]=datetime.date.today()
                     attVal["timein"]="None"
                     attVal["timeout"]=str(datetime.datetime.now().time().strftime("%I:%M %p"))
                     attVal["name"]=i["name"]
                     attVal["role"]=i["role"]
                     print("even")
            

            atten_ser=attendenceSerializer(data=attVal)
            if atten_ser.is_valid():
               atten_ser.save()
               return JsonResponse(attVal,safe=False)
            return JsonResponse("Failed to Add",safe=False)
      else:
         return JsonResponse("Invalid Member ID",safe=False)


