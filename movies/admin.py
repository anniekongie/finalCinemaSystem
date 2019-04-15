from django.contrib import admin
from movies.models import MovieInfo, Review, Showtime
# Register your models here.                                                                     




class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('movie', 'rating', 'name', 'comment', 'pub_date')
    list_filter = ['pub_date', 'name']
    search_fields = ['comment']

admin.site.register(MovieInfo)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Showtime)




