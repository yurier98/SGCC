# Generated by Django 4.1.2 on 2023-04-16 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Categoría del producto')),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
            },
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atributo', models.CharField(max_length=50, unique=True, verbose_name='Atributo')),
                ('valor', models.CharField(max_length=50, unique=True, verbose_name='Valor')),
            ],
            options={
                'verbose_name': 'Atributo',
                'verbose_name_plural': 'Atributos',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre del producto')),
                ('img', models.ImageField(blank=True, default='no_picture.jpg', null=True, upload_to='products')),
                ('state', models.CharField(choices=[('D', 'Disponible'), ('P', 'Prestado')], default='D', max_length=1, verbose_name='Estado')),
                ('stock', models.PositiveIntegerField(verbose_name='Cantidad de unidades')),
                ('active', models.BooleanField(default=True, help_text='Si no está marcado, le permitirá ocultar el producto sin eliminarlo.', verbose_name='Activo')),
                ('available', models.BooleanField(default=True, help_text='Marcar si el producto está disponible en el sistema.', verbose_name='Disponible')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.category', verbose_name='Categoria del producto')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ['-created'],
                'permissions': (('report_product', 'Puede reportar productos'),),
            },
        ),
    ]
