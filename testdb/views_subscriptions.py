# to access other domin to access our method
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser  # incoming data into data model
from django.http.response import JsonResponse
from testdb.serializer import subscriptionSerializer
from testdb.models import subscription
from testdb.models import members

@csrf_exempt
def subscriptionApi(request, id=0):
   if request.method == 'GET':
      subs = subscription.objects.all()
      # using serializer class to convert it to json
      subs_ser = subscriptionSerializer(subs, many=True)
      return JsonResponse(subs_ser.data, safe=False)
   elif request.method == 'POST':
      # passing request and using serilizer to convert it into model
      subs_data = JSONParser().parse(request)
      if (members.objects.filter(memberid=subs_data["memberid"])):
         Name = members.objects.get(memberid=subs_data["memberid"]).name
         # Email = members.objects.get(memberid=subs_data["memberid"]).email
         subs_data["name"] = Name
      subs_ser = subscriptionSerializer(data=subs_data)
      # email = Email
      name = subs_data['name']
      plan = subs_data['plan']
      startDate = subs_data['startDate']
      endPlanDate = subs_data['endPlanDate']
      paidAmt = subs_data['paidAmt']
      pendingAmt = subs_data['pendingAmt']
      sub = "Member Billing details."
      if subs_ser.is_valid():
          subs_ser.save()        
          billingid = subs_ser.data['billingid']
          if (pendingAmt == 0):
            msg= "Dear " + name + ", your Subscription plan of " + plan + " is active from " + startDate +" till "+ endPlanDate + ". You have paid an amount of "+str(paidAmt)+ ". Your billing Id is "+str(billingid)+"."         
          else:
            msg="Dear " + name + ", your Subscription plan of " + plan + " is active from "  + startDate +" till "+ endPlanDate + ". You have paid an amount of "+str(paidAmt)+" and your pending amount is "+str(pendingAmt)+ ". Your billing Id is "+str(billingid)+"."
         #  sendText.mail_bhejde(email,sub,msg)
          return JsonResponse(subs_ser.data ,safe=False) #"Added successfully",
      return JsonResponse("Billing Failed",safe=False)
   elif request.method == 'PUT':
        subs_data = JSONParser().parse(request) #1st capturing exciting record
        print(subs_data)
        subs = subscription.objects.get(billingid = subs_data['billingid'])
        print(subs)
        subs_ser = subscriptionSerializer(subs,data=subs_data)
      #   Email = members.objects.get(memberid=subs_data["memberid"]).email
        name=subs_data['name']
        billingid=subs_data['billingid']
        paidAmt=subs_data['paidAmt']
        pendingAmt=subs_data['pendingAmt']
        sub="Billing Update Alert!!"
        mesg="Dear " + name +", Your Billing details of billingId "+str(billingid)+" has been updated."+" Your total Paid Amount now is "+str(paidAmt)+" and your Pending Amount is "+str(pendingAmt)+"."
        if subs_ser.is_valid():
         subs_ser.save()
         # sendText.mail_bhejde(Email,sub,mesg)
         return JsonResponse("Bill is Updated",safe=False)
        return JsonResponse("Billing for pending amount Failed")