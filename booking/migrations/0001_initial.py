# Generated by Django 2.1.7 on 2019-04-15 04:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(default=1, primary_key=True, serialize=False)),
                ('orderid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(blank=True, default='', max_length=50)),
                ('adultQuantity', models.CharField(blank=True, default='', max_length=50)),
                ('childQuantity', models.CharField(blank=True, default='', max_length=50)),
                ('seniorQuantity', models.CharField(blank=True, default='', max_length=50)),
                ('totalSum', models.CharField(blank=True, default='', max_length=50)),
                ('adjustedSum', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentInfo',
            fields=[
                ('userAccount', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('cardNumber', models.CharField(blank=True, default='0000', max_length=50)),
                ('cardMonth', models.CharField(blank=True, default='0000', max_length=50)),
                ('cardYear', models.CharField(blank=True, default='0000', max_length=50)),
                ('cardPin', models.CharField(blank=True, default='0000', max_length=50)),
                ('cardFirstName', models.CharField(blank=True, default='', max_length=50)),
                ('cardLastName', models.CharField(blank=True, default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('promoCode', models.CharField(blank=True, default='', max_length=50, primary_key=True, serialize=False)),
                ('discount', models.CharField(blank=True, default='00', max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Showing',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('s1', models.BooleanField(default=False)),
                ('s2', models.BooleanField(default=False)),
                ('s3', models.BooleanField(default=False)),
                ('s4', models.BooleanField(default=False)),
                ('s5', models.BooleanField(default=False)),
                ('s6', models.BooleanField(default=False)),
                ('s7', models.BooleanField(default=False)),
                ('s8', models.BooleanField(default=False)),
            ],
        ),
    ]