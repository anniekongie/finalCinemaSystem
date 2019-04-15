from django.urls import path
from . import views


urlpatterns = [
    path('chooseSeats/<showing>/', views.chooseSeats,name='chooseSeats'),
    path('chooseTickets/<showing>/',views.chooseTicketType, name='chooseTickets'),
    path('confirmOrder/<orderid>/',views.confirmOrder,name='confirmOrder'),
    path('checkout/<orderid>/',views.checkout, name='checkout'),                               
    path('orderComplete/<orderid>/',views.orderComplete, name='orderComplete'),
]



