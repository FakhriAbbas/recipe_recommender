import random, string, json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


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
        'Central America',
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
