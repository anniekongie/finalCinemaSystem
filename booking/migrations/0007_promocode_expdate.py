# Generated by Django 2.1.7 on 2019-04-16 23:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_order_ispaid'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocode',
            name='expdate',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]