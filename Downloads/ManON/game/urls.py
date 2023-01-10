from django.urls import path
from . import views

urlpatterns = [

    path('getgame/', views.GameView.as_view()),
    path('search/', views.SearchPlayer.as_view()),
    path('search_history/', views.SearchHistory.as_view()),
    path('resume/', views.ResumeView.as_view()),
]
