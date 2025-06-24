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
    listing_title = serializers.CharField(source='listing.title', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'listing',
            'listing_title',
            'user_email',
            'amount',
            'reference',
            'status',
            'date_paid',
        ]
        read_only_fields = ['reference', 'status', 'date_paid']