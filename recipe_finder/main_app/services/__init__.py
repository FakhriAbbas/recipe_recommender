import random, string, json, pickle
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from ..data import *
import pandas as pd


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    result_str = result_str.upper()
    return result_str

def save_data_to_storage(user_id, page_name ,data):
    default_storage.save('./data/results/' + str(user_id) + '/' + page_name , ContentFile(json.dumps(data)))

def delete_file(user_id, page_name):
    default_storage.delete('./data/results/' + str(user_id) + '/' + page_name)

def load_data_from_storage(user_id, page_name):
    content = default_storage.open('./data/results/' + str(user_id)  + '/' + page_name , mode = 'r').readline()
    return content

def get_failure_response(exception_msg):
    response = {}
    response['statue'] = 0
    response['error-msg'] = 'Something went wrong:' + exception_msg
    return response

def get_cuisine_list():
    cuisine_list = [
        'Asian',
        'Barbecue',
        'Mediterranean',
        'North American',
        'European',
        'Oceanic',
        'Middle Eastern',
        'African',
        'North American',
        'Caribbean',
        'South American',
        'Central American',
        'Caucasian'
    ]
    return cuisine_list

def get_course_list():
    course_list = [
        'Afternoon Tea',
        'Appetizers',
        'Beverages',
        'Breads',
        'Breakfast and Brunch',
        'Cocktails',
        'Condiments and Sauces',
        'Desserts',
        'Lunch',
        'Main Dishes',
        'Salads',
        'Side Dishes',
        'Snacks',
        'Soups'
    ]
    return course_list

def get_preference(user_id):
    cuisine_list = get_cuisine_preference(user_id)
    course_list = get_course_preference(user_id)
    exclude_list = list()
    return cuisine_list, course_list, exclude_list

def get_cuisine_preference(user_id):
    preference_json = json.loads(default_storage.open('./data/results/' + str(user_id) + '/preference' , mode = 'r').readline())
    return preference_json['q1']

def get_course_preference(user_id):
    preference_json = json.loads(default_storage.open('./data/results/' + str(user_id) + '/preference' , mode = 'r').readline())
    return preference_json['q3']

def load_cuisine_df(cuisine_list):
    subset_df = pd.DataFrame()
    for c in cuisine_list:
        tmp_df = get_cuisine_df(c)
        subset_df = pd.concat([subset_df, tmp_df])
    return subset_df

def load_ingr_mlb():
    return ingr_mlb

def save_search_space(user_id, search_space_df):
    search_space_df.to_pickle(str(default_storage.location) + '/data/results/' + str(user_id) + '/search_space.pkl')

def load_search_space(user_id):
    return pd.read_pickle(str(default_storage.location) + '/data/results/' + str(user_id) + '/search_space.pkl')

def save_study_variables(user_id, dict_ = {}):
    save_data_to_storage(user_id, 'study_settings' ,  dict_ )

def add_to_study_settings(user_id, key, value):
    content = load_data_from_storage(user_id,'study_settings')
    dict = json.loads(content)
    delete_file(user_id, 'study_settings')
    dict[key] = value
    save_study_variables(user_id, dict)

def get_study_settings_value(user_id, value):
    content = load_data_from_storage(user_id, 'study_settings')
    dict = json.loads(content)
    if value in dict:
        return dict[value]
    else:
        return None

def get_user_id(request):
    return request.session.get('USER_ID')

def get_display_name(column_name):
    return display_name_dict[column_name]

def get_relevant_columns():
    return ['id','recipeName','totalTimeInMinutes', 'smallImageUrl','ingredients','course','cuisine', 'url',
                                                                               'piquant_n', 'sour_n', 'salty_n', 'sweet_n', 'bitter_n', 'meaty_n',
                                                                               'saturatedFatContent_n', 'fatContent_n',
                                                                               'carbohydrateContent_n',
                                                                               'sugarContent_n', 'calories_n',
                                                                               'fiberContent_n', 'cholesterolContent_n',
                                                                               'transFatContent_n', 'sodiumContent_n',
                                                                               'proteinContent_n'
                                                                               ]

def get_exploration_progress_service(counter):
    return 100*((counter-1)/6)

def get_meal_plan_progress_service(counter):
    return 100*((counter-1)/6)

def check_if_file_exists(user_id, page_name):
    return default_storage.exists('./data/results/' + str(user_id) + '/' + page_name)

def save_dislike_recipe_list(recipe_list, user_id):
    page_name = 'dislike_recipe_list'
    if check_if_file_exists(user_id, page_name):
        delete_file(user_id,page_name)
    save_data_to_storage(user_id, page_name, recipe_list)

def load_dislike_recipe_list(user_id):
    if not check_if_file_exists(user_id, 'dislike_recipe_list'):
        return []
    return json.loads(load_data_from_storage(user_id, 'dislike_recipe_list'))

def load_meal_plan_recipe_list(user_id):
    if not check_if_file_exists(user_id, 'meal_plan_recipe_list'):
        return []
    return json.loads(load_data_from_storage(user_id, 'meal_plan_recipe_list'))

def save_meal_plan_recipe_list(recipe_list, user_id):
    page_name = 'meal_plan_recipe_list'
    if check_if_file_exists(user_id, page_name):
        delete_file(user_id,page_name)
    save_data_to_storage(user_id, page_name, recipe_list)
