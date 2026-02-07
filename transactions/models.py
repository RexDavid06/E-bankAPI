from django.db import models
import uuid
from django.conf import settings
from wallets.models import Wallet



# Create your models here.
class Transaction(models.Model):
    STATUS = (
        ("PENDING", "Pending"),
        ("FAILED", "Failed"),
        ("SUCCESS", "Success"),
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='sent_tnx')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name='received_tnx')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    idempotency_key = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=7, choices=STATUS)
    narration = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status


class LedgerEntry(models.Model):
    ENTRY_TYPE = (
        ("DEBIT", "Debit"),
        ("CREDIT", "Credit"),
    )

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    entry_type = models.CharField(max_length=6, choices=ENTRY_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.transaction)
    
    class Meta:
        verbose_name = 'Ledger Entry'
        verbose_name_plural = 'Ledger Entries'
    


