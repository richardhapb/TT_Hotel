# Generated by Django 5.1.2 on 2024-10-23 14:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_customer_password_reset_token'),
        ('raffle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raffle',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='raffle',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='raffle',
            name='start_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='raffle',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.customer'),
        ),
    ]
