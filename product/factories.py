import factory

from product.models import Product, Category

class CategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('pystr')
    slug = factory.Faker('pystr')
    description = factory.Faker('pystr')
    active = factory.Iterator([True, False])

    class Meta:
        model = Category

class ProductFactory(factory.django.DjangoModelFactory):
    price = factory.Faker('pyint', min_value=1, max_value=100)
    title = factory.Faker('pystr')

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        if isinstance(extracted, list):
            for category in extracted:
                self.category.add(category)

    class Meta:
        model = Product
