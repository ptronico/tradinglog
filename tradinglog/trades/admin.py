from django.contrib import admin

from .models import Trade, TradeErrors


admin.site.register(Trade)
admin.site.register(TradeErrors)
