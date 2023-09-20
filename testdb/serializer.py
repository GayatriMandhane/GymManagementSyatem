from rest_framework import serializers   
from django.contrib.auth.models import User
# from testdb.models import enquiry
from testdb.models import expense, members
from dataclasses import field
from rest_framework import serializers     
from testdb.models import enquiry
from testdb.models import members
from testdb.models import attendence
from testdb.models import subscription

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user


class enquirySerializer(serializers.ModelSerializer):
   class Meta:
       model = enquiry
       fields = ('eId','eName','ephone','edate','nextDate','reason')

class membersSerializer(serializers.ModelSerializer):
   class Meta:
       model = members
       fields = ('memberid','name','email','phone','altphone','address','dob','doj','role')
    
class  attendenceSerializer(serializers.ModelSerializer):
   class Meta:
       model =  attendence
       fields = ('attendenceid','memberid','date','timein','timeout','name','role') 

class  subscriptionSerializer(serializers.ModelSerializer):
   class Meta:
       model =  subscription
       fields = ('billingid','memberid','name','plan','startDate','endPlanDate','paymentMode','paidAmt','pendingAmt') 

class expenseSerializer(serializers.ModelSerializer):
   class Meta:
       model = expense
       fields = ('expid','expAmt','date','reason')




 
       