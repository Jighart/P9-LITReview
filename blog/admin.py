from django.contrib import admin
from .models import Ticket, Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    max_num = 1
    show_change_links = True

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time_created')
    list_select_relate = ('user')
    search_fields = ('title', 'body')
    ordering = ('time_created', 'user')
    list_filter = ('time_created',)
    inlines = [ReviewInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('headline', 'user', 'ticket', 'time_created')
    list_select_relate = ('ticket', 'user')
