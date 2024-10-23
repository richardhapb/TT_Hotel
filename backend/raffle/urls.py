from django.urls import path
from raffle import views


urlpatterns = [
    path('', views.get_raffles, name='get_raffles'),
    path('create/', views.create_raffle, name='create_raffle'),
    path('finish/<int:raffle_id>/', views.finish_raffle, name='finish_raffle'),
]

