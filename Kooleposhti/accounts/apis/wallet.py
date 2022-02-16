


from accounts.models import Wallet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from accounts.permissions import IsInstructor
from accounts.serializers.user_serializers import WalletSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action

class WalletViewSet(ModelViewSet):
	queryset = Wallet.objects.all()
	serializer_class = WalletSerializer
	permission_classes = [IsAdminUser]

	def get_object(self):
	 	return self.request.user.wallet

	@action(detail=False, methods=['get', 'patch'],
	permission_classes=[IsAuthenticated])
	def mywallet(self, request, *args, **kwargs):
		if request.method == 'GET':	
			return super().retrieve(request, *args, **kwargs)
		return super().update(request, *args, **kwargs)

	@action(detail=False, methods=['post'],
	permission_classes=[IsInstructor])
	def withdraw(self, request, *args, **kwargs):
		wallet = self.get_object()
		amount = request.data['amount']
		if not wallet.is_set():
			return Response('Fill in the card-no and sheba.',
							status=status.HTTP_400_BAD_REQUEST)
		if amount > wallet.balance:
			return Response('Insufficient funds.',
							status=status.HTTP_400_BAD_REQUEST)
		if amount < 100000 or amount % 1000:
			return Response('Invalid amount.',
							status=status.HTTP_400_BAD_REQUEST)
		wallet.withdraw(amount)
		return Response('done.', status=status.HTTP_200_OK)