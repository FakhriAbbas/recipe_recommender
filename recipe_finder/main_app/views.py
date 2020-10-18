from django.shortcuts import render
from django.http import HttpResponse
from .services import *
from .logic import *
import json

def index(request):
    if 'USER_ID' not in request.session:
        request.session['USER_ID'] = get_random_string(20)
    print(request.session.get('USER_ID'))
    return render(request, 'main_app/index.html')

def pre_survey(request):
    if(request.is_ajax()):
        response = save_pre_survey_process(request)
        return HttpResponse(json.dumps(response), content_type="application/json")
    return render(request, 'main_app/pre_survey.html', context={})


def part_2_instructions(request):
    return render(request, 'main_app/part_2_instructions.html')

def preference(request):
    if(request.is_ajax()):
        response = save_preference_process(request)
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        context = {
            'cuisine_list' : get_cuisine_list(),
            'course_list' : get_course_list()
        }
        return render(request, 'main_app/preference.html', context = context)

def session_1(request):
    return render(request, 'main_app/critique_recommender.html')

def session_1_reflection(request):
    return render(request, 'main_app/critique_reflection.html')

def session_2(request):
    return render(request, 'main_app/critique_recommender_div.html')

def session_2_reflection(request):
    return render(request, 'main_app/critique_reflection_div.html')

def session_3(request):
    return render(request, 'main_app/list_recommender.html')

def session_3_reflection(request):
    return render(request, 'main_app/list_recommender_reflection.html')

def thank_you(request):
    return render(request, 'main_app/thank_you.html')
