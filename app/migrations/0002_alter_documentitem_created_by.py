# Generated by Django 3.2.20 on 2024-03-22 08:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentitem',
            name='created_by',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='DocumentItem_created_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
