# Generated by Django 3.2.20 on 2024-03-22 08:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('documentId', models.IntegerField()),
                ('inventoryId', models.IntegerField()),
                ('name', models.CharField(max_length=250)),
                ('isSync', models.BooleanField(default=False)),
                ('sync_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddIndex(
            model_name='documentitem',
            index=models.Index(fields=['documentId', 'inventoryId'], name='app_documen_documen_78f937_idx'),
        ),
    ]
