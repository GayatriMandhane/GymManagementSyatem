from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt  #to access other domin to access our method
from rest_framework.parsers import JSONParser  #incoming data into data model
from django.http.response import JsonResponse  
from rest_framework.decorators import api_view
from testdb.serializer import membersSerializer
from testdb.models import members, subscription,enquiry
# from testdb.models import dashboard
from django.http import HttpResponse
import calendar
from django.db.models import Sum
from datetime import timedelta, datetime
# Create your views here.

@csrf_exempt
def dashboardApi(request,id=0):
   if request.method == 'GET':
      dash_all=members.objects.all().values()
      dash_staff=members.objects.filter(role="staff").values()
      dash_member=members.objects.filter(role="member").values()
      dash_trainee = members.objects.filter(role="trainee").values()
      current_date=datetime.now().date()
      current_month_int = current_date.month
      current_year = current_date.year
      months = ['zero','January','February','March','April','May','June','July','August','September','October','November','December']
      current_month = months[current_month_int]
      # print(current_month)
      past3=current_date- timedelta(days=90)
      past6=current_date- timedelta(days=180)
      past1yr=current_date- timedelta(days=365)
      print("month->",current_month_int)
      if current_month_int != 10 and current_month_int != 11 and current_month_int != 12:
         first_day_of_month = str(current_year) + "-" + "0" + str(current_month_int) +"-"+"01"
      else:
         first_day_of_month = str(current_year) + "-" + str(current_month_int) +"-"+"01"
      # print("return :",threeM)
      threeM1=members.objects.filter(doj__gte=past3).filter(doj__lte=current_date)
      sixMonth=members.objects.filter(doj__gte=past6).filter(doj__lte=current_date)
      one_year=members.objects.filter(doj__gte=past1yr).filter(doj__lte=current_date)
      new_admission=members.objects.filter(doj__gte=first_day_of_month).filter(doj__lte=current_date)

      all_ser = membersSerializer(dash_all,many=True) 
      staff_ser = membersSerializer(dash_staff,many=True)
      member_ser= membersSerializer(dash_member,many=True) 
      trainee_ser=membersSerializer(dash_trainee,many=True) 
      three_ser=membersSerializer(threeM1,many=True)
      six_ser=membersSerializer(sixMonth,many=True)
      past1_ser=membersSerializer(one_year,many=True)
      new_admission_ser=membersSerializer(new_admission,many=True)

      Total_Fees_Collected = subscription.objects.aggregate(Sum('paidAmt'))
      Total_Pending_Fees = subscription.objects.aggregate(Sum('pendingAmt'))
      Total_Fees_Collection = Total_Fees_Collected['paidAmt__sum'] + Total_Pending_Fees['pendingAmt__sum']

      #birthday count code 
      today = datetime.now().date()
      tomorrow = today + timedelta(1)
      today = str(today)
      tomorrow = str(tomorrow)
      bday_count = 0
      for i in dash_all:
         bday = str(i['dob'])
         if today[4:]==bday[4:] or tomorrow[4:]==bday[4:]:
            bday_count = bday_count +1

      #pending bill count 
      pending_bill_count=subscription.objects.exclude(pendingAmt="0").count()

      #Enquiry count code
      all_enquiry = enquiry.objects.all().values()
      enquiry_count = 0
      for i in all_enquiry:
            date = str(i['nextDate'])
            if today==date or tomorrow==date:
               enquiry_count = enquiry_count +1
      
   #Code for member with expiring or expired membership
      subscription_data = subscription.objects.all().values()
      dateVal=[]
      for i in range(0,len(all_ser.data)):
         dateVal=[]
         for j in range(0,len(subscription_data)):
            if all_ser.data[i]['memberid']==subscription_data[j]['memberid']:
               dateVal.append(subscription_data[j]['endPlanDate'])
         if dateVal:
            latest_date=max(dateVal)
            all_ser.data[i]['endPlanDate']=latest_date
         else:
            all_ser.data[i]['endPlanDate']='No Data'
      
      today = datetime.now().date()
      tomorrow = today + timedelta(1)
      expiry_count = 0
      inactive =0
      active = 0
      for i in all_ser.data:
         expday = str(i['endPlanDate'])
         if expday!="No Data":
            expday1 = datetime.strptime(expday,'%Y-%m-%d').date()
            if today==expday1 or tomorrow==expday1 or today>expday1:
               expiry_count = expiry_count +1

            if today>expday1:
               inactive = inactive +1
            else:
               active = active +1

      #using serializer class to convert it to json
      return JsonResponse({"all":all_ser.data,
      "staff":staff_ser.data,
      "member":member_ser.data,
      "trainee":trainee_ser.data,
      "three_month":three_ser.data,
      "six_month":six_ser.data,
      "one_year":past1_ser.data,
      "new_admission":new_admission_ser.data,
      "birthday_count":bday_count,
      "pending_bill_count":pending_bill_count,
      "enquiry_count":enquiry_count,
      "Total_Fees_Collection":Total_Fees_Collection, 
      "Total_Fees_Collected":Total_Fees_Collected['paidAmt__sum'],
      "Total_Pending_Fees":Total_Pending_Fees['pendingAmt__sum'],
      "Expiring_Subscription":expiry_count,
      "Inactive":inactive,
      "Active":active},safe=False)
      

     


      
