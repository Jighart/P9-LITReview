from django.contrib import admin
from .models import Ticket, Review

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time_created')
    search_fields = ('title', 'body')
    ordering = ('time_created', 'user')
    list_filter = ('time_created',)

admin.site.register(Review)
# admin.site.register(UserFollow)