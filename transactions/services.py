from django.db import transaction
from .models import Transaction
from wallets.models import Wallet
from decimal import Decimal
from .models import LedgerEntry


class InsufficientFund(Exception):
    pass

@transaction.atomic
def transfer_funds(*, sender, receiver, amount, narration=None, idempotency_key):
    if Transaction.objects.filter(idempotency_key=idempotency_key).exists():
        return Transaction.objects.get(idempotency_key=idempotency_key)
    
    sender_wallet = Wallet.objects.select_for_update().get(user=sender)
    receiver_wallet = Wallet.objects.select_for_update().get(user=receiver)

    if sender_wallet.balance < amount:
        raise InsufficientFund("insufficient balance for this transaction")
    
    sender_wallet.balance -= Decimal(amount)
    receiver_wallet.balance += Decimal(amount)

    sender_wallet.save()
    receiver_wallet.save()

    tx = Transaction.objects.create(
        sender=sender,
        receiver=receiver,
        amount=amount,
        narration=narration,
        idempotency_key=idempotency_key,
        status = "SUCCESS"
    )
    LedgerEntry.objects.bulk_create([
        LedgerEntry(
            transaction=tx,
            wallet=sender_wallet,
            amount=amount,
            entry_type="DEBIT",
        ),
        LedgerEntry(
            transaction=tx,
            wallet=receiver_wallet,
            amount=amount,
            entry_type="CREDIT",
        )
    ])
    
    return tx