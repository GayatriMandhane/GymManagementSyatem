from django.views.decorators.csrf import csrf_exempt #to access other domin to access our method
from django.http.response import JsonResponse
#from postgresTest import testdb
from testdb.serializer import membersSerializer, subscriptionSerializer,enquirySerializer
from testdb.models import members,enquiry,subscription
from datetime import timedelta, datetime


@csrf_exempt
def notification(request,id=0):
    if request.method == 'GET':
        # Code for Birthday for today and tomorrow 
        all_member = members.objects.all().values()
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today = str(today)
        tomorrow = str(tomorrow)
        bdaylist = []
        for i in all_member:
            bday = str(i['dob'])
            if today[4:]==bday[4:] or tomorrow[4:]==bday[4:]:
                bdaylist.append(i)
        Bday_ser = membersSerializer(bdaylist,many=True)
        for i in Bday_ser.data:
            bday=str(i['dob'])
            if today[4:]==bday[4:]:
               i['day']="Today"
            else:
                i['day']="Tomorrow"

        #Code for member with expiring or expired membership
        dash_all=members.objects.all()
        all_ser = membersSerializer(dash_all,many=True) 
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
        # print(all_ser.data)
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        expirylist = []
        for i in all_ser.data:
            expday = str(i['endPlanDate'])
            if expday!="No Data":
                expday1 = datetime.strptime(expday,'%Y-%m-%d').date()
                if today==expday1 or tomorrow==expday1 or today>expday1:
                    expirylist.append(i)
                    if today==expday1:
                        i['day']="Today"
                    elif tomorrow==expday1:
                        i['day']="Tomorrow"
                    elif today>expday1:
                        i['day']="expired"
                    else:
                        i['day']="active"

        # Code for pending payment bill members 
        pending_bill=subscription.objects.exclude(pendingAmt="0")
        pending_bill_ser = subscriptionSerializer(pending_bill,many=True)

        # Code for next day Enquiry
        all_enquiry = enquiry.objects.all().values()
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today = str(today)
        tomorrow = str(tomorrow)
        enqList=[]
        for i in all_enquiry:
            date = str(i['nextDate'])
            if today==date or tomorrow==date:
                enqList.append(i)
        enq_ser= enquirySerializer(enqList,many=True)
        for i in enq_ser.data:
            date=str(i['nextDate'])
            if today==date:
               i['day']="Today"
            else:
                i['day']="Tomorrow"
        print(enq_ser.data)
        return JsonResponse({
            "Birthday":Bday_ser.data,
            "Pending_bill":pending_bill_ser.data,
        "upcoming_enquiry":enq_ser.data,
        "expiring_membership":expirylist
        },safe=False)