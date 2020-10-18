import random, string
from ..services import *
from django.urls import reverse

def save_pre_survey_process(request):
    response = {}
    try:
        # read responses
        q1 = request.POST.get("q1", "")
        q2 = request.POST.getlist("q2[]")
        q2_text = request.POST.get("q2_text", "")
        q3 = request.POST.get("q3", "")
        q4 = request.POST.getlist("q4[]")
        q4_text = request.POST.get("q4_text", "")
        q5 = request.POST.get("q5", "")
        q6 = request.POST.get("q6", "")

        # prepare data
        data = {}
        data['q1'] = q1
        data['q2'] = q2
        data['q2_text'] = q2_text
        data['q3'] = q3
        data['q4'] = q4
        data['q4_text'] = q4_text
        data['q5'] = q5
        data['q6'] = q6

        # save data
        save_data_to_storage(request.session.get('USER_ID'), page_name='pre_survey' , data = data)

        # prepare success response
        response['status'] = 1
        response['redirect-url'] = reverse('part_2_instructions')
        return response
    except Exception as e:
        # prepare failure response
        return get_failure_response(exception_msg = e.strerror)

def save_preference_process(request):
    response = {}
    try:
        # read responses
        q1 = request.POST.getlist("q1[]")
        q3 = request.POST.getlist("q3[]")

        # prepare data
        data = {}
        data['q1'] = q1
        data['q3'] = q3

        # save data
        save_data_to_storage(request.session.get('USER_ID') , page_name='preference', data = data)

        # prepare success response
        response['status'] = 1
        response['redirect-url'] = reverse('session_1')
        return response
    except Exception as e:
        # prepare failure response
        return get_failure_response(exception_msg = e.strerror)
