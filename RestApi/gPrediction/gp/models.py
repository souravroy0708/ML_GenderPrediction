from django.db import models

COMMON_STATUS=(
              ('0','INACTIVE'),
              ('1','ACTIVE'),
              )

class BaseInfo(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,default='1',choices=COMMON_STATUS,help_text='Category Status')

    class Meta:
        abstract = True	

class Enquiry(BaseInfo):
    ip_address = models.CharField(max_length=128,null=True,blank=True,help_text='user ip address')
    name = models.CharField(null=True,blank=True,max_length=128,help_text='First Name')
    prediction = models.CharField(null=True,blank=True,max_length=128,help_text='Predictions')
    
    def __unicode__(self):
       return str(self.name)
