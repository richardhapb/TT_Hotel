from django.urls import path
from customers import views



urlpatterns = [
    # POST
    path('', views.new_user_input, name='new_user_input'),
    # GET
    path('', views.CustomerViewSet.as_view({'get': 'list'}), name='list'),
    # PUT
    path('<int:pk>', views.CustomerViewSet.as_view({'put': 'update'}), name='update'),
    # DELETE
    path('<int:pk>', views.CustomerViewSet.as_view({'delete': 'destroy'}), name='destroy'),
]


