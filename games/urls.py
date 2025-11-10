# games/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('new/', views.new_game, name='new_game'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('game/<int:game_id>/move/', views.make_move_view, name='make_move'),
    path('game/<int:game_id>/delete/', views.delete_game, name='delete_game'),
]