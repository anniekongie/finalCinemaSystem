from django.contrib import admin
from booking.models import Showing, PromoCode, TicketSetting, Order, PaymentInfo
from booking.forms import paymentForm

from accounts.models import UserInfo
from django.core.mail import send_mail
from django.core import mail 
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

#admin.site.register(Review, ReviewAdmin)                                                        
admin.site.register(Showing)

admin.site.register(TicketSetting)
admin.site.register(Order)
# Register your models here.                                                                     
admin.site.register(PaymentInfo)

def send_promo(self,request,queryset):
        for query in queryset:
            send_promo.short_description = 'Send promo email to subscribed users'
            recipientList=UserInfo.objects.filter(sendPromo=True).values_list('email',flat=True)
            promocode=query.promoCode
            discount =query.discount

            mail_subject='Promo code for you!'
            message=render_to_string('promo_email.html', {
                    'promoCode':promocode,
                    'discount':discount,
                    })
            email=EmailMessage(mail_subject, message, to=recipientList)
            email.send()


class paymentFormAdmin(admin.ModelAdmin):
    def save(self, request, obj, form, change):
        obj.userAccount = request.user
        obj.save()

class PromoCodeAdmin(admin.ModelAdmin):
    actions=[send_promo]


admin.site.register(PromoCode,PromoCodeAdmin)
