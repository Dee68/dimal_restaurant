from django.contrib import admin
from .models import Review, Reservation, Table


admin.site.register(Table)
admin.site.register(Reservation)
admin.site.register(Review)
