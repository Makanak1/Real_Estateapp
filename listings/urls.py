from django.urls import path
from .views import ManageListingView, ListingDetailView, ListingsView, SearchListingsView, MakeInquiryView, PayForListingView, InquiryListView, PaymentListView ,VerifyPaymentView,PaymentView 
urlpatterns = [
    path('manage/', ManageListingView.as_view()),
    path('detail/', ListingDetailView.as_view()),
    path('get-listings/', ListingsView.as_view()),
    path('search/', SearchListingsView.as_view()),
    path('inquiry/', MakeInquiryView.as_view(), name='make-inquiry'),
    path('payment/<int:id>/', PaymentView.as_view(),name='payment'),
    path('payment/initialize', PayForListingView.as_view(), name='pay-listing'),
    path('verify-payment/<str:ref>/', VerifyPaymentView.as_view()),
    path('admin/inquiries/', InquiryListView.as_view(), name='admin-inquiries'),
    path('admin/payments/', PaymentListView.as_view(), name='admin-payments'),
]