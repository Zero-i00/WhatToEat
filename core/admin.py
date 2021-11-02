from django.contrib import admin
from django.urls import path
from core.models import *
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.conf.urls import url
from scrapers.tasks import create_sources

# Register your models here.

admin.site.register(Ingredient)
admin.site.register(Recipe)

@admin.register(Dishes)
class ParserAdmin(admin.ModelAdmin):
    change_list_template = "core/admin_changes.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('parser/parse/parsing/', self.parse),
        ]
        return my_urls + urls

    def parse(self, request):
        create_sources.delay()
        self.message_user(request, "Parsing...")
        return HttpResponseRedirect("../")

