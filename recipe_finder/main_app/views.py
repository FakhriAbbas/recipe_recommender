from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from .logic import *
import json

def index(request):
    if 'USER_ID' not in request.session:
        request.session['USER_ID'] = get_random_string(20)
    save_study_variables(get_user_id(request))
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
    context = {}
    add_to_study_settings(get_user_id(request), 'current_session' , 'session_1')
    if request.is_ajax():
        pass
    else:
        result_json, result_df, search_space_df = init_critique_recommender(request)
        result_json = generate_critique_static(result_df, search_space_df)
        context['items'] = result_json
        session_1_counter = get_study_settings_value(get_user_id(request), 'session_1_counter')
        if session_1_counter is None:
            add_to_study_settings(get_user_id(request), 'session_1_counter' , 1)
        session_1_counter = get_study_settings_value(get_user_id(request), 'session_1_counter')
        current_session = get_study_settings_value(get_user_id(request), 'current_session')
        save_data_to_storage(get_user_id(request),
                             current_session  + '_' + str(session_1_counter),
                             result_json )
        context['session_progress'] = get_exploration_progress_service(session_1_counter)
        context['meal_plan_progress'] = get_meal_plan_progress(get_user_id(request))
        return render(request, 'main_app/critique_recommender_parent.html', context = context)

# Not used
def submit_like_dislike(request):
    if request.is_ajax():
        response = {}
        template = get_template("main_app/includes/recipe_list_shopping.html")
        response['list-content'] = template.render({'items': request.session.get('items')}, request)
        template = get_template("main_app/includes/shopping_cart_direction.html")
        response['direction-content'] = template.render({},request)
        template = get_template("main_app/includes/button_shopping.html")
        response['button-content'] = template.render({},request)
        response['status'] = 1
        return HttpResponse(json.dumps(response), content_type="application/json")

def submit_dislike_add_to_plan(request):
    if request.is_ajax():
        response = {}
        template = get_template("main_app/includes/recipe_list_critique.html")
        items = load_current_results(request)
        response['list-content'] = template.render({'items': items }, request)
        template = get_template("main_app/includes/critique_header.html")
        context = {}
        session_1_counter = get_study_settings_value(get_user_id(request), 'session_1_counter')
        context['session_progress'] = get_exploration_progress_service(session_1_counter)
        context['meal_plan_progress'] = get_meal_plan_progress(get_user_id(request))
        response['direction-content'] = template.render(context,request)
        template = get_template("main_app/includes/empty.html") # TODO based on progress
        response['button-content'] = template.render({},request)
        response['status'] = 1
        return HttpResponse(json.dumps(response), content_type="application/json")

# Not used
def submit_shopping(request):
    if request.is_ajax():
        response = {}
        template = get_template("main_app/includes/recipe_list_critique.html")
        response['list-content'] = template.render({
                                                    'items': request.session.get('items')
                                                    },
                                                    request)
        template = get_template("main_app/includes/critique_direction.html")
        response['direction-content'] = template.render({},request)
        response['status'] = 1
        return HttpResponse(json.dumps(response), content_type="application/json")

def load_critique(request):
    if request.is_ajax():
        response = {}
        recipe_id, critique_list = get_critique_for_recipe( request )
        template = get_template("main_app/includes/critique_list.html")
        response['critique-content'] = template.render({"critiques" : critique_list , 'recipe_id' : recipe_id }, request)
        response['status'] = 1
        return HttpResponse(json.dumps(response), content_type="application/json")

def submit_load_more(request):
    if request.is_ajax():
        response = {}
        json_result, result_df  = load_more_critique_recommender(request)
        result_json = generate_critique_static(result_df, load_search_space(get_user_id(request)))
        template = get_template("main_app/includes/recipe_list_critique.html")
        response['list-content'] = template.render({'items': result_json }, request)
        template = get_template("main_app/includes/critique_header.html")
        context = {}
        session_1_counter = get_study_settings_value(get_user_id(request), 'session_1_counter')
        context['session_progress'] = get_exploration_progress_service(session_1_counter)
        context['meal_plan_progress'] = get_meal_plan_progress(get_user_id(request))
        response['direction-content'] = template.render(context,request)
        template = get_template("main_app/includes/empty.html") # TODO based on progress
        response['button-content'] = template.render({},request)
        response['status'] = 1

        current_session = get_study_settings_value(get_user_id(request), 'current_session')
        if current_session == 'session_1':
            session_1_counter = get_study_settings_value(get_user_id(request), 'session_1_counter')
            add_to_study_settings(get_user_id(request), 'session_1_counter' , session_1_counter + 1)
            session_1_counter = get_study_settings_value(get_user_id(request), 'session_1_counter')
            save_data_to_storage(get_user_id(request),
                             current_session  + '_' + str(session_1_counter),
                             result_json )
        return HttpResponse(json.dumps(response), content_type="application/json")

def submit_dislike(request):
    response = {}
    recipe_name = request.POST.get("recipe_name", "")
    user_id = get_user_id(request)
    if request.POST.get("value", "") == '0':
        print('maybe')
        remove_dislike_recipe(recipe_name,user_id)
    elif request.POST.get("value", "") == '1':
        add_dislike_recipe(recipe_name,user_id)
    response['status'] = 1
    return HttpResponse(json.dumps(response), content_type="application/json")

def submit_add_to_meal(request):
    response = {}
    recipe_name = request.POST.get("recipe_name", "")
    user_id = get_user_id(request)
    counter = 0
    if request.POST.get("value", "") == '0':
        counter = remove_recipe_add_to_meal_plan(recipe_name,user_id)
    elif request.POST.get("value", "") == '1':
        counter = add_recipe_add_to_meal_plan(recipe_name,user_id)
    response['status'] = 1
    response['meal_plan_progress'] = get_meal_plan_progress(get_user_id(request))
    return HttpResponse(json.dumps(response), content_type="application/json")

def show_meal_plan(request):
    if request.is_ajax():
        response = {}
        template = get_template("main_app/includes/meal_plan_modal.html")
        items = get_meal_plan_recipes(request)
        response['model_template'] = template.render({
                                                    'items': items
                                                    },
                                                    request)
        response['status'] = 1
        return HttpResponse(json.dumps(response), content_type="application/json")

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
