from django.urls import path
from customers import views



urlpatterns = [
    path('', views.new_user_input, name='new_user_input'),
    path('', views.CustomerViewSet.as_view({'get': 'list'}), name='list'),
    path('<int:pk>', views.CustomerViewSet.as_view({'put': 'update'}), name='update'),
    path('<int:pk>', views.CustomerViewSet.as_view({'delete': 'destroy'}), name='destroy'),
    path('login/', views.login, name='login'),
    path('refresh/', views.refresh, name='refresh'),
    path('logout/', views.logout, name='logout'),
    path('set_password/', views.set_password, name='set_password'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('change_password/', views.change_password, name='change_password'),
]


