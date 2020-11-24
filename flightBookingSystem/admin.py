from django.contrib import admin

# Register your models here.

from .models import Flight, Ticket

admin.site.register(Flight)
admin.site.register(Ticket)

