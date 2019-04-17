from django.shortcuts import render, redirect
from django.http import HttpResponse
from movies.models import MovieInfo, Review, Showtime
from .models import Showing, Order, PromoCode, TicketSetting, PaymentInfo
from django.urls import reverse
from .forms import SeatsForm, ticketsForm, paymentForm
from django.contrib.auth.decorators import login_required
from datetime import datetime

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import send_mail

# Create your views here.                                                                                                                

def chooseSeats(request,showing):
    print('showing:',showing)
    obj=Showing.objects.get(id=int(showing))
    ogform=SeatsForm(instance=obj)

    if request.method=='POST':
        formFields=request.POST
        form = SeatsForm(request.POST)
        print('form',form)
        if form.is_valid():
            form.save()
            showid=int(showing)
            showing=Showing.objects.get(id=showid)
            print('showingobj: ',showing)

            '''showing.s1=form.cleaned_data['s1']
            showing.s2=form.cleaned_data['s2']
            showing.s3=form.cleaned_data['s3']
            showing.s4=form.cleaned_data['s4']
            showing.s5=form.cleaned_data['s5']
            showing.s6=form.cleaned_data['s6']
            showing.s7=form.cleaned_data['s7']
            showing.s8=form.cleaned_data['s8']
            showing.save()
            '''
            tixform=ticketsForm()

        return render(request,'selecttickets.html',{'form':tixform, 'showing':showing})

    else:
        form=SeatsForm(instance=obj)
        context={
            'form':form,
            'showing':obj,
            }
        return render(request, 'seats.html', context)

def chooseTicketType(request,showing):
    obj=Showing.objects.get(id=int(showing))
    movieObj=obj.showtime.movie
    print('obj',obj)
    print('showing used to get obj:',showing)
    print('movieObj:',movieObj)

    ticketSetting=TicketSetting.objects.get(movie=movieObj)
    fee=float(ticketSetting.fee)
    if request.method=='POST':
        form=ticketsForm(request.POST)
        if form.is_valid():
            adultQuantity=int(form.cleaned_data['adultQuantity'])
            childQuantity=int(form.cleaned_data['childQuantity'])
            seniorQuantity=int(form.cleaned_data['seniorQuantity'])
            userAccount=request.user.id
            date = obj.showtime.time
            title=movieObj.title
            totalTicket=(adultQuantity*ticketSetting.adultPrice)+(childQuantity*ticketSetting.childPrice) + (seniorQuantity*ticketSetting.seniorPrice)
            salesTax=round((totalTicket*(7/100)),2)
            totalSum=salesTax+totalTicket+fee
            order=Order()
            print('uuid: ',order.orderid)
            order.adultQuantity=adultQuantity
            order.childQuantity=childQuantity
            order.seniorQuantity=seniorQuantity
            order.userAccount=request.user
            order.date=date
            order.title=title
            order.totalSum=totalSum        
            order.save()            
            print('showing aka obj.id: ',obj.id)
            print('order.orderid',order.orderid)
            context={
                'adult':adultQuantity,
                'child':childQuantity,
                'senior':seniorQuantity,
                'showing':obj.id,
                'order':order,
                'adultPrice': ticketSetting.adultPrice,
                'childPrice': ticketSetting.childPrice,
                'seniorPrice': ticketSetting.seniorPrice,
                'userAccount': userAccount,
                'orderid': order.orderid,
                'fee':ticketSetting.fee,
                }
            return render(request,'totalsum.html',context)

def confirmOrder(request,orderid):
    orderObj=Order.objects.get(orderid=orderid)

    print('orderObj', orderObj)
    movieObj=MovieInfo.objects.get(title=orderObj.title)
    ticketSetting=TicketSetting.objects.get(movie=movieObj)
    ticketSettingcopy=ticketSetting
    promo=None
    discountedRate=0.0
    if request.method=='POST':
        promoCode = request.POST.get('promo','')
        promoExists=PromoCode.objects.filter(promoCode__exact=promoCode)
        if promoExists.expdate >= datetime.now():
            promoExists=None
        if promoExists:
            promo = PromoCode.objects.get(promoCode__exact=promoCode)
            discount=int(promo.discount)/100
            discountedRate=float(orderObj.totalSum)*discount
            adjustedCost=round(float(orderObj.totalSum)-discountedRate,2)
            print('adjusted Cost',adjustedCost)
            print('orderObj.userAccount:', orderObj.userAccount)
            print('orderid: ', orderid)
            orderObj.adjustedSum=str(adjustedCost)
            print('order\'s adjusted sum: ', orderObj.adjustedSum)
            orderObj.save()
            print('orderObj.id passed to checkout',orderObj.id)
        context={
            'promo':promo,
            'order':orderObj,
            'subtractValue': discountedRate,
            'adult': orderObj.adultQuantity,
            'child': orderObj.childQuantity,
            'senior':orderObj.seniorQuantity,
            'adultPrice': ticketSettingcopy.adultPrice,
            'childPrice': ticketSettingcopy.childPrice,
            'seniorPrice': ticketSettingcopy.seniorPrice,
            'adjustedTotal': orderObj.adjustedSum,
            'fee':ticketSettingcopy.fee,
            'orderid':orderObj.orderid,
            }
        return render(request,'totalsum.html',context)
    else:
        return HttpResponse('You\'ve lost you\'re current session. Please start a new booking')


@login_required
def checkout(request,orderid):
    orderObj=Order.objects.get(orderid=orderid)
    title=orderObj.title
    movieObj=MovieInfo.objects.get(title=title)
    adjustedSum = orderObj.adjustedSum
    ticketSetting=TicketSetting.objects.get(movie=movieObj)
    showtime=orderObj.date 
   
    curruser=orderObj.userAccount
    paymentInfo=PaymentInfo.objects.filter(userAccount=curruser)

    if request.method=='POST': #if submit is clicked
        print('in checkout view...')
        form=paymentForm(request.POST,instance=PaymentInfo(userAccount=curruser))
        if form.is_valid():
            paymentObj=form.save()
            orderObj.isPaid=True
            orderObj.save()
            

            #sending confrimation email
            user=orderObj.userAccount.first_name
            totalsum=orderObj.totalSum
            adults=orderObj.adultQuantity
            child=orderObj.childQuantity
            senior= orderObj.seniorQuantity
            totalSeats=int(adults)+int(child)+int(senior)
            print('totalseats:', totalSeats)
            mail_subject='We\'ve recieved your order!'
            message=render_to_string('orderconfirmed_email.html', {
                    'user': user,
                    'adjusted':adjustedSum,
                    'total':totalsum,
                    'adult':adults,
                    'child':child,
                    'senior':senior,
                    'showtime':showtime,
                    'title':title,
                    'totalSeats':totalSeats,
                    'orderid': orderObj.orderid,
                    })
            reciever=orderObj.userAccount.email
            print('email: ', reciever)
            email=EmailMessage(mail_subject, message, to=[reciever])
            email.send()
            #emal sent 


            context={
                'title':title,
                'total':adjustedSum,
                'ticketSetting':ticketSetting,
                'order':orderObj,
                'showtime':showtime,
                'payment':paymentObj,
                }
            return render(request,'confirm.html',context)
    else: #when you first come to this page
        if paymentInfo:
            payment=paymentInfo[0]
            form=paymentForm(instance=payment)
        else:
            form=paymentForm()
            context={
                'title':title,
                'ticketSetting':ticketSetting,
                'order':orderObj,
                'showtime':showtime,
                'form':form,
                }
        return render(request,'checkout.html',{'form':form})
         

def orderComplete(request,orderid):
    orderObj=Order.objects.get(orderid=orderid)
    context={
        'order':order,
        }
    return render(request,'orderComplete.html',context)
    
    
        
        
