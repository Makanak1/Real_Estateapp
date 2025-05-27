from rest_framework import serializers
from .models import Listing
from .models import Inquiry, Payment

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields ='__all__'
        
class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'
        read_only_fields = ['date_sent']
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['date_paid']