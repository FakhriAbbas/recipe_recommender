from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'main_app/index.html')

def pre_survey(request):
    return render(request, 'main_app/pre_survey.html')

def part_2_instructions(request):
    return render(request, 'main_app/part_2_instructions.html')

def preference(request):
    return render(request, 'main_app/preference.html')

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
