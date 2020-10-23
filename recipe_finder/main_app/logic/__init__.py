import random, string
from ..services import *
from django.urls import reverse
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist


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
    request.session.get('USER_ID')
    # load preference
    cuisine_list , course_list , _ = get_preference(request.session.get('USER_ID'))
    # generate recommendation
    recommended_recipes = generate_recommendation(cuisine_list, course_list, N = 10)
    json_result = json.loads(recommended_recipes.to_json(orient='records'))
    # save result

    return json_result

def generate_recommendation(cuisine_list, course_list, N = 10):
    subset_df = load_cuisine_df(cuisine_list)
    ingr_mlb = load_ingr_mlb()
    centroid = subset_df[ingr_mlb.classes_].mean()
    distance_ = cdist([centroid], subset_df[ingr_mlb.classes_], metric='euclidean')[0]
    distance_ = (distance_ - min(distance_)) / (max(distance_) - min(distance_))
    subset_df['dist_'] = distance_ / 2
    subset_df['course_score'] = (np.sum(subset_df[course_list].values, axis=1) / len(course_list)) / 2
    subset_df['score'] = subset_df['dist_'] + subset_df['course_score']
    top_n_recipe = subset_df.sort_values(by='score', ascending=False)[0:N*10][['id','recipeName','totalTimeInMinutes', 'smallImageUrl','ingredients','course','cuisine', 'url']]
    top_n_recipe.drop_duplicates(subset=['id'], inplace=True)
    return top_n_recipe[0:N]

def generate_critique_static():
    # create dataframe
    df_critique = pd.DataFrame(columns=['column_name', 'display_name', 'direction'])

    flavor_col =  ['piquant', 'sour', 'salty', 'sweet', 'bitter', 'meaty',]
    nutrition_col = [ 'saturatedFatContent', 'fatContent', 'carbohydrateContent',
                    'sugarContent', 'calories', 'fiberContent', 'cholesterolContent',
                    'recipeYield', 'transFatContent', 'sodiumContent', 'proteinContent']
    col_list = flavor_col # + nutrition_col
    for col in col_list:
        new_row = {'column_name': col, 'display_name': col, 'direction': 'Less'}
        df_critique = df_critique.append(new_row, ignore_index=True)
        new_row = {'column_name': col, 'display_name': col, 'direction': 'More'}
        df_critique = df_critique.append(new_row, ignore_index=True)

    json_result = json.loads(df_critique.to_json(orient='records'))
    return json_result
