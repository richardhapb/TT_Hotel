# admin.py

from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from raffle.models import Raffle
from django.http import HttpResponseRedirect

class RaffleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'start_date', 'end_date', 'winner', 'finish_raffle_link')

    # Método que genera el enlace de 'Finalizar rifa' si aún no hay ganador
    def finish_raffle_link(self, obj):
        if not obj.winner:  # Solo muestra el enlace si no hay ganador
            url = reverse('finish_raffle', args=[obj.id])
            return format_html('<a href="{}">Finalizar</a>', url)
        return 'Sorteo finalizado'

    finish_raffle_link.short_description = 'Finalizar Rifa'

    # Método para definir URLs personalizadas en el admin
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('finish/<int:raffle_id>/', self.admin_site.admin_view(self.finish_raffle), name='finish_raffle'),
        ]
        return custom_urls + urls

    # Lógica para finalizar la rifa
    def finish_raffle(self, request, raffle_id):
        return HttpResponseRedirect(reverse('finish_raffle', args=[raffle_id]))


admin.site.register(Raffle, RaffleAdmin)