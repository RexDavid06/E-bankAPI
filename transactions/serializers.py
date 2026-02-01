from rest_framework import serializers
from .models import LedgerEntry


class TransferSerializer(serializers.Serializer):
    receiver_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    idempotency_key = serializers.CharField()


class LedgerEntrySerializer(serializers.ModelSerializer):
    transaction_id = serializers.UUIDField(source='transaction.id')
    class Meta:
        model = LedgerEntry
        fields = ['transaction_id', 'wallet', 'amount', 'entry_type', 'created_at']

