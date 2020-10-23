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