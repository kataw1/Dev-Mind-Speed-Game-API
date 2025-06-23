from django.urls import path
from .views import start_game, submit_answer, end_game

urlpatterns = [
    path('game/start', start_game, name='start_game'),
    path('game/<uuid:game_id>/submit', submit_answer, name='submit_answer'),
    path('game/<uuid:game_id>/end', end_game, name='end_game'),
]
