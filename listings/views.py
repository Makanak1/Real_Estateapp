import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Listing
from .serializers import ListingSerializer
import traceback
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from rest_framework.generics import ListAPIView
from .serializers import InquirySerializer, PaymentSerializer
from .models import Inquiry, Payment
from django.shortcuts import get_object_or_404


class ManageListingView(APIView):
    def get(self, request, format=None): 
        try:
            user = request.user

            if not user.is_realtor:
                return Response(
                    {'error': 'user does not have necessary permissions for geting the Listing data'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            slug = request.query_params.get('slug')

            if not slug:
                listing = Listing.objects.order_by('-date_created').filter(realtor=user.email)
                
                listing = ListingSerializer(listing, many=True)

                return Response(
                    {'listings': listing.data},
                    status=status.HTTP_200_OK
                )
    
            if not Listing.objects.filter(
                realtor=user.email,
                slug=slug
            ).exists():
                return Response(
                    {'error': 'Listing not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            listing = Listing.objects.get(
                realtor=user.email,
                slug=slug
            )
            listing = ListingSerializer(listing)
            return Response(
                {'listing': listing.data},
                status=status.HTTP_200_OK
            )

        except:
            return Response(
                {'error': 'Something went wrong when fetching listing'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve_values(self, data):
        title = data['title']
        slug = data['slug']
        address = data['address']
        city = data['city']
        state = data['state']
        zip_code = data['zip_code']
        description = data['description']


        price = data['price']
        try:
            price = int(price)
        except:
            return Response(
                {'error': 'price must be an integer'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        bedrooms = data['bedrooms']
        try:
            bedrooms = int(bedrooms)
        except:
            return Response(
                {'error': 'bedrooms must be an integer'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        bathrooms = data['bathrooms']
        try:
            bathrooms = float(bathrooms)
        except:
            return Response(
                {'error': 'bathrooms must be a floating point value'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if bathrooms <= 0 or bathrooms >= 10:
            bathrooms = 1.0

        bathrooms = round(bathrooms, 1)

        sale_type = data['sale_type']

        if sale_type == 'FOR_RENT':
            sale_type = 'For Rent'
        else:
            sale_type = 'For Sale'

        home_type = data['home_type']
        
        if home_type == 'CONDO':
            home_type = 'Condo'
        elif home_type == 'TOWNHOUSE':
            home_type = 'Townhouse'
        else:
            home_type = 'House'
        
        main_photo = data['main_photo']
        photo_1 = data['photo_1']
        photo_2 = data['photo_2']
        photo_3 = data['photo_3']
        is_published = data['is_published']

        if is_published == 'True':
            is_published = True
        else:
            is_published = False
            
            
        data = {
            'title': title,
            'slug': slug,
            'address': address,
            'city': city,
            'state': state,
            'zip_code': zip_code,
            'description': description,
            'price': price,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'home_type': home_type,
            'sale_type': sale_type,
            'main_photo': main_photo,
            'photo_1': photo_1,
            'photo_2': photo_2,
            'photo_3': photo_3,
            'is_published': is_published
        }
        return data
    
    
    def post(self, request):
        try:
            user = request.user

            if not user.is_realtor:
                return Response(
                    {'error': 'user does not have necessary permissions for creating the Listing data'},
                    status=status.HTTP_403_FORBIDDEN
                )
            data = request.data
            
            data = self.retrieve_values(data)
            
            title = data['title']
            slug = data['slug']
            address = data['address']
            city = data['city']
            state = data['state']
            zip_code = data['zip_code']
            description = data['description']
            price = data['price']
            bedrooms = data['bedrooms']
            bathrooms = data['bathrooms']
            sale_type = data['sale_type']
            home_type = data['home_type']
            main_photo = data['main_photo']
            photo_1 = data['photo_1']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3']
            is_published = data['is_published']
            
            
            if Listing.objects.filter(slug=slug).exists():
                return Response(
                    {'error': 'Listing with this slug already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            
            Listing.objects.create(
                realtor=user.email,
                title=title,
                slug=slug,
                address=address,
                city=city,
                state=state,
                zip_code=zip_code,
                description=description,
                price=price,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                home_type=home_type,
                sale_type=sale_type,
                main_photo=main_photo,
                photo_1=photo_1,
                photo_2=photo_2,
                photo_3=photo_3,
                is_published=is_published
            )

            return Response(
                {'success': 'Listing created successfully'},
                status=status.HTTP_201_CREATED
            )

        except:
            return Response(
                {'error': 'Something went wrong when creating listing'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request):
        try:
            user = request.user

            if not user.is_realtor:
                return Response(
                    {'error': 'user does not have necessary permissions for updating the Listing data'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            data = request.data
            
            data = self.retrieve_values(data)
            
            title = data['title']
            slug = data['slug']
            address = data['address']
            city = data['city']
            state = data['state']
            zip_code = data['zip_code']
            description = data['description']
            price = data['price']
            bedrooms = data['bedrooms']
            bathrooms = data['bathrooms']
            sale_type = data['sale_type']
            home_type = data['home_type']
            main_photo = data['main_photo']
            photo_1 = data['photo_1']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3']
            is_published = data['is_published']
            
            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response(
                    {'error': 'Listing does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            Listing.objects.filter(realtor=user.email, slug=slug).update(
                title=title,
                slug=slug,
                address=address,
                city=city,
                state=state,
                zip_code=zip_code,
                description=description,
                price=price,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                home_type=home_type,
                sale_type=sale_type,
                main_photo=main_photo,
                photo_1=photo_1,
                photo_2=photo_2,
                photo_3=photo_3,
                is_published=is_published
            )
            return Response(
                {'success': 'Listing updated successfully'},
                status=status.HTTP_200_OK
            )
            

        except Exception as e:
            traceback.print_exc()  # This prints the stack trace to the console
            return Response(
                {'error': f'Something went wrong when updating listing: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def patch(self, request):
        try:
            user = request.user
            
            if not user.is_realtor:
                return Response(
                    {'error': 'user does not have necessary permissions for updating the Listing data'},
                    status=status.HTTP_403_FORBIDDEN
                )
            data = request.data
            
            slug = data['slug']
            
            is_published = data['is_published']
            if is_published == 'True':
                is_published = True
            else:
                is_published = False
                
            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response(
                    {'error': 'Listing does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            Listing.objects.filter(realtor=user.email, slug=slug).update(
                is_published=is_published
            )
            
            return Response(
                {'success': 'Listing  publish status updated successfully'},
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            traceback.print_exc()  # This prints the stack trace to the console
            return Response(
                {'error': f'Something went wrong when updating listing: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request):
        try:
            user = request.user
            
            if not user.is_realtor:
                return Response(
                    {'error': 'user does not have necessary permissions for deleting the Listing data'},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            data = request.data
            
            try:
                slug = data['slug']
            except:
                return Response(
                    {'error': 'slug was not provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response(
                    {'error': 'Listing you are trying to delete does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            Listing.objects.filter(realtor=user.email, slug=slug).delete()
            
            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response(
                    {'success': 'Listing deleted successfully'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Failed to delete listing'},
                    status=status.HTTP_400_BAD_REQUEST 
                )
                
        except Exception as e:
            traceback.print_exc()  # This prints the stack trace to the console
            return Response(
                {'error': f'Something went wrong when deleting listing: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
                

class ListingDetailView(APIView):
    def get(self, request, format=None):
        try:
            slug = request.query_params.get('slug')
            if not slug:
                return Response(
                    {'error': 'Must provide a slug'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not Listing.objects.filter(slug=slug, is_published=True).exists():
                return Response(
                    {'error': 'Published listing  with this slug does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
            listing = Listing.objects.get(slug=slug, is_published=True)
            listing = ListingSerializer(listing)
            return Response(
                {'listing': listing.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Error retrieving listing'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class ListingsView(APIView):
    def get(self, request, format=None):
        try:
            if not Listing.objects.filter(is_published=True).exists():
                return Response(
                    {'error': 'No published listings in the database'},
                    status=status.HTTP_404_NOT_FOUND
                )
            listings = Listing.objects.filter(is_published=True).order_by('-date_created')
            listings = ListingSerializer(listings, many=True)
            return Response(
                {'listings': listings.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving listings'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class SearchListingsView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request, format=None):
        try:
            search = request.query_params.get('search')
            
            listings = Listing.objects.annotate(
                search=SearchVector('title', 'description', 'address', 'city', 'state', 'zip_code')
            ).filter(
                search=SearchQuery(search),
                is_published=True
            ).order_by(
                SearchRank('search', SearchQuery(search))
            )
            
            print('Listings:')
            print(listings)
            for listing in listings:
                print(listing.title)
            
            return Response(
                {'success': 'Everything went ok'},
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            traceback.print_exc()  # This prints the stack trace to the console
            return Response(
                {'error': f'Something went wrong when searching for  listing: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
class MakeInquiryView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            data = request.data
            slug = data.get('slug')
            email = data.get('email')
            message = data.get('message')

            if not (slug and email and message):
                return Response(
                    {'error': 'slug, email, and message are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                listing = Listing.objects.get(slug=slug, is_published=True)
            except Listing.DoesNotExist:
                return Response(
                    {'error': 'Listing not found or unavailable'},
                    status=status.HTTP_404_NOT_FOUND
                )

            Inquiry.objects.create(
                listing=listing,
                user_email=email,
                message=message
            )

            return Response(
                {'success': 'Inquiry sent successfully'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': f'Error making inquiry: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class PayForListingView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            data = request.data
            slug = data.get('slug')
            email = data.get('email')
            amount = data.get('amount')
            reference = data.get('reference')

            if not (slug and email and amount and reference):
                return Response(
                    {'error': 'slug, email, amount, and reference are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                listing = Listing.objects.get(slug=slug, is_published=True)
            except Listing.DoesNotExist:
                return Response(
                    {'error': 'Listing not found or already unavailable'},
                    status=status.HTTP_404_NOT_FOUND
                )

            if Payment.objects.filter(reference=reference).exists():
                return Response(
                    {'error': 'This payment reference has already been used'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            Payment.objects.create(
                listing=listing,
                user_email=email,
                amount=amount,
                reference=reference
            )

            # Mark the listing as no longer published
            listing.is_published = False
            listing.save()

            return Response(
                {'success': 'Payment successful. Listing marked as unavailable.'},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': f'Something went wrong during payment: {str(e)}'},  
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class InquiryListView(ListAPIView):
    queryset = Inquiry.objects.all().order_by('-date_sent')
    serializer_class = InquirySerializer
    permission_classes = [permissions.IsAdminUser]


class PaymentListView(ListAPIView):
    queryset = Payment.objects.all().order_by('-date_paid')
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAdminUser]

class VerifyPaymentView(APIView):
    def get(self, request, ref):
        try:
            order = get_object_or_404(Listing, ref=ref)
            url = f'https://api.paystack.co/transaction/verify/{ref}'
            headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
            response = requests.get(url, headers=headers)  # Use requests library instead of request
            response_data = response.json()
            if response_data["status"] and response_data["data"]["status"] == "success":
                order.payment_complete = True
                order.save()
                return Response({"Message": "Payment verified successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"Error": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)
        except Listing.DoesNotExist:
            return Response({'error': 'Invalid payment reference'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
