# Generated by Django 5.1.2 on 2024-10-23 04:23

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_customer_email_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='password_reset_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True, unique=True),
        ),
    ]
