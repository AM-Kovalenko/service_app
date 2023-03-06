from django.contrib import admin

from services.models import Services, Plan, Subscriptions

admin.site.register(Services)
admin.site.register(Plan)
admin.site.register(Subscriptions)
