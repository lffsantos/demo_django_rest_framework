from django.contrib import admin


from log_entries.core.models import Category, Event


admin.site.register(Category)
admin.site.register(Event)