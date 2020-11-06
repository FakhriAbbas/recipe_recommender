import random, string
from ..services import *
from django.urls import reverse
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
import math


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

def init_critique_recommender(request):
    user_id = request.session.get('USER_ID')
    # load preference
    cuisine_list , course_list , _ = get_preference(request.session.get('USER_ID'))
    # generate recommendation
    recommended_recipes, search_space_df = generate_recommendation(cuisine_list, course_list, user_id, N = 10)
    save_search_space(user_id, search_space_df)
    json_result = json.loads(recommended_recipes.to_json(orient='records'))
    return json_result, recommended_recipes, search_space_df

def generate_recommendation(cuisine_list, course_list, user_id, N = 10):
    subset_df = load_cuisine_df(cuisine_list)
    ingr_mlb = load_ingr_mlb()
    centroid = subset_df[ingr_mlb.classes_].mean()
    distance_ = cdist([centroid], subset_df[ingr_mlb.classes_], metric='euclidean')[0]
    distance_ = (distance_ - min(distance_)) / (max(distance_) - min(distance_))
    subset_df['dist_'] = distance_ / 2
    if len(course_list) != 0:
        subset_df['course_score'] = (np.sum(subset_df[course_list].values, axis=1) / len(course_list)) / 2
    else:
        subset_df['course_score'] = 0
    subset_df['score'] = subset_df['dist_'] + subset_df['course_score']
    top_n_recipe = subset_df.sort_values(by='score', ascending=False)[0:N*10][get_relevant_columns()]
    top_n_recipe.drop_duplicates(subset=['id'], inplace=True)

    # add dislike and meal values
    top_n_recipe = top_n_recipe[0:N]
    top_n_recipe['dislike'] = [1 if v in load_dislike_recipe_list(user_id) else 0 for v in top_n_recipe.id.values]
    top_n_recipe['meal_plan'] = [1 if v in load_meal_plan_recipe_list(user_id) else 0 for v in top_n_recipe.id.values]
    return top_n_recipe, subset_df

def generate_critique_static(result_df, search_space_df):
    flavor_col =  ['piquant_n', 'sour_n', 'salty_n', 'sweet_n', 'bitter_n', 'meaty_n']
    nutrition_col = [ 'saturatedFatContent_n', 'fatContent_n', 'carbohydrateContent_n',
                    'sugarContent_n', 'calories_n', 'fiberContent_n', 'cholesterolContent_n',
                    'transFatContent_n', 'sodiumContent_n', 'proteinContent_n']
    result_df['critique'] = None
    result_df['critique'].astype('object')

    for index, row in result_df.iterrows():
        df_critique = pd.DataFrame(columns=['column_name', 'display_name', 'direction'])

        for col in flavor_col:
            if not math.isnan(row[col]):
                has_more = (search_space_df[col].values > row[col]).any()
                has_less = (search_space_df[col].values < row[col]).any()
                if has_more:
                    new_row = {'column_name': col, 'display_name': get_display_name(col), 'direction': 'More'}
                    df_critique = df_critique.append(new_row, ignore_index=True)
                if has_less:
                    new_row = {'column_name': col, 'display_name': get_display_name(col), 'direction': 'Less'}
                    df_critique = df_critique.append(new_row, ignore_index=True)

        for col in nutrition_col:
            s = search_space_df[col].values
            if row[col]:
                has_more = ( s > row[col] ).any()
                has_less = ( s < row[col] ).any()
                if has_more:
                    new_row = {'column_name': col, 'display_name': get_display_name(col), 'direction': 'More'}
                    df_critique = df_critique.append(new_row, ignore_index=True)
                if has_less:
                    new_row = {'column_name': col, 'display_name': get_display_name(col), 'direction': 'Less'}
                    df_critique = df_critique.append(new_row, ignore_index=True)

        result_df.at[index,'critique'] = json.loads( df_critique.to_json(orient='records') )

    json_result = json.loads(result_df.to_json(orient='records'))
    return json_result

def get_critique_for_recipe(request):
    results_json = load_current_results(request)
    recipe_id = request.POST.get('recipe_name')
    for recipe in results_json:
        if recipe['id'] == recipe_id:
            return recipe_id, recipe['critique']
    return None

def load_current_results(request):
    user_id = get_user_id(request)
    session_name = get_study_settings_value(user_id, 'current_session')
    if session_name == 'session_1':
        session_counter = get_study_settings_value(user_id, 'session_1_counter')
    results_json = json.loads(load_data_from_storage(user_id, str(session_name) + '_' + str(session_counter)))

    dislike_result = load_dislike_recipe_list(user_id)
    meal_plan_result = load_meal_plan_recipe_list(user_id)
    for recipe in results_json:
        if recipe['id'] in dislike_result:
            recipe['dislike'] = 1
        else:
            recipe['dislike'] = 0
        if recipe['id'] in meal_plan_result:
            recipe['meal_plan'] = 1
        else:
            recipe['meal_plan'] = 0

    return results_json

def load_more_critique_recommender(request):
    user_id = request.session.get('USER_ID')
    direction = request.POST.get("direction", "")
    column_name = request.POST.get("critique_name", "")
    recipe_name = request.POST.get("recipe_name", "")

    # load preference
    cuisine_list , course_list , _ = get_preference(request.session.get('USER_ID'))
    # generate recommendation
    recommended_recipes = load_more_recipes(cuisine_list, course_list, direction, column_name, recipe_name, user_id, N = 10)
    json_result = json.loads(recommended_recipes.to_json(orient='records'))
    return json_result, recommended_recipes

def load_more_recipes(cuisine_list, course_list, direction, column_name, recipe_name, user_id, N = 10):
    search_space_df = load_search_space(user_id)
    threshold = search_space_df[search_space_df['id'] == recipe_name][column_name].values[0]
    if direction == 'More':
        tmp_df = search_space_df[ search_space_df[column_name] > threshold ]
    elif direction == 'Less':
        tmp_df = search_space_df[search_space_df[column_name] < threshold]
    centroid = tmp_df[ tmp_df['id'] == recipe_name ][ingr_mlb.classes_].mean()
    distance_ = cdist([centroid], tmp_df[ingr_mlb.classes_], metric='euclidean')[0]
    distance_ = (distance_ - min(distance_)) / (max(distance_) - min(distance_))
    tmp_df.loc[:, 'dist_'] = distance_ / 2
    if len(course_list) != 0:
        tmp_df.loc[ : , 'course_score'] = (np.sum(tmp_df[course_list].values, axis=1) / len(course_list)) / 2
    else:
        tmp_df.loc[ : , 'course_score'] = 0.0
    tmp_df.loc[ : , 'score'] = tmp_df['dist_'] + tmp_df['course_score']
    top_n_recipe = tmp_df.sort_values(by='score', ascending=False)[0:N*10][get_relevant_columns()]
    top_n_recipe.drop_duplicates(subset=['id'], inplace=True)
    top_n_recipe = top_n_recipe[0:N]

    # add dislike and meal values
    top_n_recipe['dislike'] = [1 if v in load_dislike_recipe_list(user_id) else 0 for v in top_n_recipe.id.values]
    top_n_recipe['meal_plan'] = [1 if v in load_meal_plan_recipe_list(user_id) else 0 for v in top_n_recipe.id.values]
    return top_n_recipe

def get_exploration_progress(counter):
    return get_exploration_progress_service(counter)

def remove_dislike_recipe(recipe_name, user_id):
    recipe_list = load_dislike_recipe_list(user_id)
    if recipe_name in recipe_list:
        recipe_list.remove(recipe_name)
        save_dislike_recipe_list(recipe_list, user_id)

def add_dislike_recipe(recipe_name, user_id):
    recipe_list = load_dislike_recipe_list(user_id)
    if recipe_name not in recipe_list:
        recipe_list.append(recipe_name)
        save_dislike_recipe_list(recipe_list, user_id)

def remove_recipe_add_to_meal_plan(recipe_name,user_id):
    recipe_list = load_meal_plan_recipe_list(user_id)
    if recipe_name in recipe_list:
        recipe_list.remove(recipe_name)
        save_meal_plan_recipe_list(recipe_list, user_id)
    return len(recipe_list)

def add_recipe_add_to_meal_plan(recipe_name,user_id):
    recipe_list = load_meal_plan_recipe_list(user_id)
    if recipe_name not in recipe_list:
        recipe_list.append(recipe_name)
        save_meal_plan_recipe_list(recipe_list, user_id)
    return len(recipe_list)

def get_meal_plan_progress(user_id):
    recipe_list = load_meal_plan_recipe_list(user_id)
    return get_meal_plan_progress_service(len(recipe_list))
