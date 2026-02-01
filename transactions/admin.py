from django.contrib import admin
from .models import Transaction, LedgerEntry

# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['amount', 'idempotency_key', 'status']

class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ['entry_type', 'amount']


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(LedgerEntry, LedgerEntryAdmin)
