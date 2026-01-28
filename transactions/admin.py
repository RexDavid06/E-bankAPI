from django.contrib import admin
from .models import Transaction

# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['amount', 'idempotency_key', 'status']

admin.site.register(Transaction, TransactionAdmin)
