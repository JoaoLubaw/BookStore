from rest_framework.viewsets import ModelViewSet

from product.models import Category
from product.serializers import CategorySerializer

class CategoryViewset(ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()
