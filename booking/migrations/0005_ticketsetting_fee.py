# Generated by Django 2.1.7 on 2019-04-15 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_auto_20190415_0139'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketsetting',
            name='fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
