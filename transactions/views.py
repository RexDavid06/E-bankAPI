from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import TransferSerializer
from django.contrib.auth import get_user_model
from .services import transfer_funds
from rest_framework.response import Response

User=get_user_model()



class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receiver = User.objects.get(id=serializer.validated_data['receiver_id'])

        tx = transfer_funds(
            sender=request.user,
            receiver=receiver,
            amount=serializer.validated_data['amount'],
            idempotency_key=serializer.validated_data['idempotency_key'],
        )
        return Response({
            "transaction_id": tx.id,
            "status": tx.status,
        })