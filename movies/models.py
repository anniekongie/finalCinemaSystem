from django.db import models
from datetime import date, datetime
from django.db.models import Avg
from booking.models import Showing, TicketSetting

# Create your models here.                                                                      \
                                                                                                 

class MovieInfo(models.Model):
    title = models.CharField(max_length=50, blank=True, default='', primary_key=True)
    releaseDate = models.DateField(blank=True, null=True)
    director = models.CharField(max_length=50, blank=True, default='')
    summary = models.CharField(max_length=550, blank=True, default='')
    poster = models.ImageField(null=True, blank=True, upload_to='posters/%m/%d/%Y')
    cast = models.CharField(max_length=100, blank=True, default='')
    rating = models.FloatField(null=True, blank=True, default=None)
    genre = models.CharField(max_length=20, blank=True, default='')
    trailer=models.CharField(max_length=300, blank=True,default='')
    
    
    def is_now_playing(self):
        if self.releaseDate < date.today():
            return True
        elif self.releaseDate == date.today():
            return True
        else:
            return False

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    movie = models.ForeignKey(MovieInfo, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    name = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)
    
    
class Showtime(models.Model):
    time = models.DateTimeField(null=True, blank=True)
    movie = models.ForeignKey(MovieInfo, on_delete=models.CASCADE, null=True)
    showing = models.OneToOneField(Showing, on_delete=models.CASCADE,null=False, default=None)
    def format_time(self):
        return time.strftime("%H:%M")


