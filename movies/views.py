from django.shortcuts import render, get_object_or_404
from .models import MovieInfo, Review, Showtime
from .forms import ReviewForm
from django.urls import reverse
import datetime
from django.db.models import Q
from django.db.models import Avg

from django.http import HttpResponseRedirect
# Create your views here.                                                                        


def viewMovie(request, title):
    movieObj = MovieInfo.objects.get(title=title)
    review_list=Review.objects.filter(movie=title).order_by('pub_date')

    #getting average rating:                                                                     
    m=movieObj
    m_reviews=m.review_set.filter(movie=title)
    avgdict=m_reviews.aggregate(Avg('rating'))
    avgrating=avgdict.get('rating__avg')
    m.rating=avgrating
    m.save()

    #get showtimes                                                                               
    showtimes=Showtime.objects.filter(movie=title)
    movie = get_object_or_404(MovieInfo, pk=title)
    form = ReviewForm()
    context={
        'movie': movieObj,
        'review_list':review_list,
        'form':form,
        'showtimes':showtimes,
        }
 #to handle searches in movieview page                                                        
    if request.method=='POST':
        results=None;
        query = request.POST['query']
        if len(query)!=0:
            results = MovieInfo.objects.filter(Q(title__icontains=query) | Q(director__icontains\
=query))
            context={
                'movies': results,
                'query':query,
                }
            return render(request, 'searchResults.html', context)

    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        name = form.cleaned_data['name']
        review = Review()
        review.movie = movie
        review.name = name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        return HttpResponseRedirect(reverse('viewMovie', args=(title,)))
    return render(request, 'movieInfo.html', context)


   # return render(request, 'movieInfo.html', context)                                           

def movieSearch(request):
    print('IN MOVIESEARCHVIEW')
    movieObj=None;
    if request.method =='POST':
        query = request.POST['query']
        if len(query)==0:
            movieObj=MovieInfo.objects.all()
            return render(request, 'searchResults.html', {'movies':movieObj})
        else:
            results = MovieInfo.objects.filter(Q(title__icontains=query) | Q(director__icontains=query))
            context={
                'movies': results,
                'query':query,
                }
            return render(request, 'searchResults.html', context)
    else:
        movieObj=MovieInfo.objects.all()
        return render(request, 'home.html', {'movies': movieObj})

def movieList(request):
    if request.method=='POST':
        searchText=request.POST.get('searchText','')
        filt1=request.POST.get('filter1',False)
        filt2=request.POST.get('filter2',False)
        filt3=request.POST.get('filter3',False)
        ###                                                                                      
        if len(searchText)!=0: #if search text exists                                            
            movieList=MovieInfo.objects.filter(Q(title__icontains=searchText) | Q(director__icontains=searchText))
            context={
                'movies': movieList
                }
            return render(request,'movieList.html',context)

        else:#if no search text, do filter stuff                                                 
            movieList=MovieInfo.objects.filter(Q(genre__icontains=filt1) |Q(genre__icontains=filt2) | Q(genre__icontains=filt3))
            context={
                'movies': movieList,
                }
            return render(request, 'movieList.html', context)
        
    else:
        movieList=MovieInfo.objects.all()
        return render(request, 'movieList.html',{'movies':movieList})
