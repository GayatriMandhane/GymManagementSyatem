from django.db import models
from django.core.validators import MinLengthValidator, int_list_validator
# Create your models here.

# class access(models.Model):
#     userid = models.CharField(max_length=20)
#     password = models.CharField(max_length=20)

class members(models.Model):
    memberid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=40,null=True)
    phone = models.CharField(verbose_name="Phone number", max_length=10,validators=[int_list_validator(sep=''),MinLengthValidator(10),], default='1234567890')
    altphone = models.CharField(verbose_name="Alternate Phone number", max_length=10,validators=[int_list_validator(sep=''),MinLengthValidator(10),],null=True)
    address = models.CharField(max_length=50)   
    dob = models.DateField()
    doj = models.DateField()
    role = models.CharField(max_length=10) 

class enquiry(models.Model):
    eId = models.AutoField(primary_key=True)
    eName = models.CharField(max_length=20)
    ephone = models.CharField(verbose_name="Phone number", max_length=10,validators=[int_list_validator(sep=''),MinLengthValidator(10),], default='1234567890')
    edate = models.DateField()
    nextDate = models.DateField()
    reason=models.CharField(max_length=50)

class subscription(models.Model):
    billingid = models.AutoField(primary_key=True)
    memberid = models.IntegerField() 
    name = models.CharField(max_length=20)
    plan = models.CharField(max_length=10)
    startDate = models.DateField()
    endPlanDate = models.DateField()
    paymentMode = models.CharField(max_length=10)
    paidAmt = models.IntegerField()
    pendingAmt = models.IntegerField() 

class attendence(models.Model):
    attendenceid = models.AutoField(primary_key=True)
    memberid = models.IntegerField() 
    date = models.DateField()
    timein = models.CharField(max_length=20)
    timeout = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    role = models.CharField(max_length=10) 
   
class expense(models.Model):
    expid = models.AutoField(primary_key=True)
    expAmt = models.IntegerField() 
    date = models.DateField()
    reason = models.CharField(max_length=100)



    

    

   
      
     