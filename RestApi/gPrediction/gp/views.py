from __future__ import division
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_auth,logout
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime, timedelta,date
import socket

from gp.models import Enquiry

from nltk.corpus import names
import random
import nltk
import pandas as pd
from nltk import NaiveBayesClassifier,classify

import logging
logger = logging.getLogger(__name__)

def index(request):
    """
    Gender Prediction index page
    """
    no_record_count = range(10)
    return render(request, 'index.html',{"no_record_count":no_record_count})


def gender_features(word):
	"""
	Get feature
	"""
	word = word.upper()
	last_letter= word[-1]
	last_two  = word[-2] 
	result = {
	            'last_letter':last_letter,
	            'last_two':last_two
	          }
	return result

def get_gender_predictions(name_input):
	"""
	Get Prediction
	"""
	try:
		train_data = ([(name, 'male') for name in names.words('male.txt')] \
	    	+ [(name, 'female') for name in names.words('female.txt')])
		mix_dataset = random.shuffle(train_data)
	        featuresets = [(gender_features(n), gender) for (n, gender) in train_data]
		# classifier = nltk.NaiveBayesClassifier.train(featuresets)
		total_record = len(train_data)
		train_set, test_set = featuresets[int(total_record*.99):], featuresets[:int(total_record*.01)]
		classifier = nltk.NaiveBayesClassifier.train(train_set)
		prediction = classifier.classify(gender_features(name_input))
	except:
	    prediction = "NA"
	return prediction

def get_search_result(request):
    """
    Function to get Gender Prediction
    """
    name_text = request.GET.get("names",None)
    
    return_object=[]
    name_input="NA"
    prediction_output = "NA"
    status = 0
    if name_text:
            name_list = name_text.split(",")
	    try:
	    	ip_address = socket.gethostbyname(socket.gethostname())
	    except:
	    	ip_address = "NA"
	        logger.exception("Error in get system ip address")
	    name_list = [str(name) for name in name_list]
	    for name_input  in name_list:
	    	if len(name_input) > 2:
		    	prediction_output = get_gender_predictions(name_input)
		    	try:
		    		Enquiry.objects.create(ip_address=ip_address,name=name_input,prediction=prediction_output)    	
		    	except:
		            logger.exception("Error in insert enquiry data")
		        status=1
		else:
		    	message="Name soluld be atleast 4 character"
	        return_object.append({"name":name_input,"prediction":prediction_output,'status':status})
    else:
    	return_object.append({"name":name_input,"prediction":prediction_output,'status':status})
    return_object_final = {"result":return_object}
    return HttpResponse(json.dumps(return_object_final),
            content_type="application/json")
