from django.contrib import admin
from gp.models import Enquiry

class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name','prediction','ip_address','created_date')
    search_fields = ['ip_address','name','prediction']
    list_filter = ('ip_address','name','prediction')
admin.site.register(Enquiry,EnquiryAdmin)