from django.urls import path
from .views import *  
urlpatterns = [
    path('manage/', ManageListingView.as_view()),
    path('detail/', ListingDetailView.as_view()),
    path('get-listings/', ListingsView.as_view()),
    path('search/', SearchListingsView.as_view()),
    path('inquiry/', MakeInquiryView.as_view(), name='make-inquiry'),
    path('initialize/payment', InitiatePaymentView.as_view(), name='pay-listing'),
    path('verify/payment/<str:ref>/', VerifyPaymentView.as_view()),
    path('admin/inquiries/', InquiryListView.as_view(), name='admin-inquiries'),
    path('admin/payments/', PaymentListView.as_view(), name='admin-payments'),
]