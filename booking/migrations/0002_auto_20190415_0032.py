# Generated by Django 2.1.7 on 2019-04-15 04:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movies', '0001_initial'),
        ('booking', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketSetting',
            fields=[
                ('movie', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='movies.MovieInfo')),
                ('adultPrice', models.IntegerField(blank=True, default=0)),
                ('childPrice', models.IntegerField(blank=True, default=0)),
                ('seniorPrice', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='userAccount',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]