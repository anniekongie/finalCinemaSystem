from django.urls import path
from . import views


urlpatterns = [
    path('searchresult/',views.movieSearch,name='movieSearch'),
    path('movies/results/',views.movieList,name='movieList'),
    path('<str:title>/', views.viewMovie,name='viewMovie'),
]




