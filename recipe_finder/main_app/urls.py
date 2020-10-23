from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pre_survey', views.pre_survey, name='pre_survey'),
    path('part_2_instructions', views.part_2_instructions, name='part_2_instructions'),
    path('preference', views.preference, name='preference'),
    path('session_1', views.session_1, name='session_1'),
    path('session_1_reflection', views.session_1_reflection, name='session_1_reflection'),
    path('session_2', views.session_2, name='session_2'),
    path('session_2_reflection', views.session_2_reflection, name='session_2_reflection'),
    path('session_3', views.session_3, name='session_3'),
    path('session_3_reflection', views.session_3_reflection, name='session_3_reflection'),
    path('thank_you', views.thank_you, name='thank_you'),
    path('submit_like_dislike', views.submit_like_dislike, name='submit_like_dislike'),
    path('submit_shopping', views.submit_shopping, name='submit_shopping'),
]