from django.db import models
from django.utils import timezone
class userDetails(models.Model):
	
	Username 	= models.CharField(max_length=100,default=None,null=True)
	Password 	= models.CharField(max_length=100,default=None,null=True)
	Name 		= models.CharField(max_length=100,default=None,null=True)
	Age 		= models.CharField(max_length=200,default=None,null=True)
	Phone 		= models.CharField(max_length=100,default=None,null=True)
	Email 		= models.CharField(max_length=100,default=None,null=True)
	Address 	= models.CharField(max_length=100,default=None,null=True)
	

	class Meta:
		db_table = 'userDetails'

class filedetails(models.Model):
    sender_name =  models.CharField(max_length=50,default=None,null=True)
    image = models.FileField(upload_to='images/', null=True)
    secret_msg = models.FileField(null=True)
    key = models.CharField(max_length=50,default=None,null=True)
    encrypt_image = models.FileField(upload_to='encrypt_image/',null=True)
    User_name = models.CharField(max_length=50,default=None,null=True)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
	    db_table = 'filedetails'