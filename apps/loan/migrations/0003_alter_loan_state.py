# Generated by Django 4.1.2 on 2023-10-24 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0002_alter_loan_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='state',
            field=models.CharField(choices=[('P', 'Pendiente a autorización'), ('PR', 'Prestado'), ('A', 'Atrasado'), ('E', 'Entregado')], default='P', max_length=2, verbose_name='Estado'),
        ),
    ]
