from django import forms
from django.forms import ModelForm
from .models import Showing,Order, PaymentInfo

QUANTITY = (('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
            ('5', '5'))

class SeatsForm(ModelForm):
    class Meta:
        model=Showing
        fields=['s1','s2','s3','s4','s5','s6','s7','s8']

class ticketsForm(forms.Form):
    adultQuantity=forms.ChoiceField(choices=QUANTITY,label='Adult: ',widget=forms.Select(),required=False)
    childQuantity=forms.ChoiceField(choices=QUANTITY,label='Child: ',widget=forms.Select(),required=False)
    seniorQuantity=forms.ChoiceField(choices=QUANTITY,label='Senior: ',widget=forms.Select(),required=False)

class paymentForm(ModelForm):
    class Meta:
        model=PaymentInfo
        fields=['cardNumber','cardMonth','cardYear', 'cardPin','cardFirstName','cardLastName' ]
        exclude=['userAccount']
