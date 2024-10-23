from django.urls import path
from raffle import views
from django.contrib.auth.decorators import user_passes_test


admin_only = user_passes_test(lambda u: u.is_superuser)

urlpatterns = [
    path('', admin_only(views.get_raffles), name='get_raffles'),
    path('create/', admin_only(views.create_raffle), name='create_raffle'),
    path('finish/<int:raffle_id>/', admin_only(views.finish_raffle), name='finish_raffle'),
]

