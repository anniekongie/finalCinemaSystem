from django.urls import path
from . import views


urlpatterns = [
    path('searchresult/',views.movieSearch,name='movieSearch'),
    path('movielist/',views.movieList,name='movieList'),
    path('movies/<str:title>/', views.viewMovie,name='viewMovie'),
]




