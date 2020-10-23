import pickle
from django.core.files.storage import default_storage

ingr_mlb = pickle.load( default_storage.open('./data/pickles/ingr_mlb.pkl', mode='rb') )
# recommender_df = pickle.load( default_storage.open( './data/pickles/recommender_df.pkl', mode='rb' ) )
cuisine_dict = {}

def load_cuisine_data_to_dict(cuisine):
    if cuisine not in cuisine_dict:
        tmp_df = pickle.load(default_storage.open('./data/pickles/recommender_df_' + str(cuisine) + '.pkl' , mode='rb'))
        cuisine_dict[cuisine] = tmp_df

def get_cuisine_df(cuisine):
    load_cuisine_data_to_dict(cuisine)
    return cuisine_dict[cuisine]


