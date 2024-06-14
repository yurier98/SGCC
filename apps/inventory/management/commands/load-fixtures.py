import itertools
from random import randint
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.inventory.models import Product, Category


class Builder:
    def __init__(self):
        self._product_count = itertools.count()

    def product(self, name=None, stock=None, commit=False):
        product_count = next(self._product_count)
        # Obtener una categoría aleatoria
        random_category = Category.objects.order_by('?').first()

        product = Product(
            name=name or f"Product {product_count}",
            category= random_category ,
            stock=stock or randint(1, 50),
        )
        if commit:
            product.save()
        return product


class Command(BaseCommand):
    help = "Removes all data and creates default products in the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "-c",
            "--count",
            nargs="?",
            dest="count",
            type=int,
            help="Number of products to create",
            default=100,
        )

    @transaction.atomic
    def handle(self, *args, count, **options):
        call_command("flush", interactive=False)
        builder = Builder()
        products = [builder.product() for _ in range(count)]
        Product.objects.bulk_create(products)

        self.stdout.write(self.style.SUCCESS('Productos creados con éxito!'))
