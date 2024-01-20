from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from order.models import Order
from order.serializers import OrderSerializer
import logging

logger = logging.getLogger(__name__)

class OrderViewSet(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by('id')

    def list(self, request, *args, **kwargs):
        logger.debug(f"Request user: {request.user}")

        # Your logic to get or serialize data
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        # Create a Response instance
        return Response(serializer.data, status=status.HTTP_200_OK)
