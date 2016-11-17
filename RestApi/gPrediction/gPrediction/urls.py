"""gPrediction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from gp import views as gp_views
admin.site.site_header = 'Gender Predictipon'
urlpatterns = [
    url(r'^admin/', admin.site.urls),   
	url(r'^get-gender-prediction/$', gp_views.get_search_result, name='get-gp-result'),
    url(r'$', gp_views.index, name='index'),   
]
