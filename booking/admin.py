from django.contrib import admin
from booking.models import Showing, PromoCode, TicketSetting, Order, PaymentInfo




#admin.site.register(Review, ReviewAdmin)                                                        
admin.site.register(Showing)
admin.site.register(PromoCode)
admin.site.register(TicketSetting)
admin.site.register(Order)
# Register your models here.                                                                     
admin.site.register(PaymentInfo)




