# Generated by Django 4.0.2 on 2022-09-14 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('success', 'success'), ('info', 'info'), ('wrong', 'wrong')], default='info', max_length=20)),
                ('object_id_actor', models.PositiveIntegerField()),
                ('verbo', models.CharField(max_length=220)),
                ('read', models.BooleanField(default=False)),
                ('publico', models.BooleanField(default=True)),
                ('eliminado', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('actor_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificar_actor', to='contenttypes.contenttype')),
                ('destiny', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notificaciones', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
                'abstract': False,
            },
        ),
    ]
