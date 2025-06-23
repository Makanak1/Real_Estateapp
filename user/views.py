from django.contrib.auth import get_user_model
user = get_user_model()
from .serializers import UserSerializer, UserUpdateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status 
from . utils import send_Email
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            data = request.data

            name = data['name']
            email = data['email']
            email = email.lower()
            password = data['password']
            re_password = data['re_password']
            is_realtor = data['is_realtor']

            if is_realtor == 'True':
                is_realtor = True
            else:
                is_realtor = False

            if password == re_password:
                if len(password) >= 8:
                    if not user.objects.filter(email=email).exists():
                        if not is_realtor:
                            user.objects.create_user(name=name, email=email, password=password)
                            send_Email(email)
                            return Response({
                                    "message":f"{name} logged in successfully",
                                    "access_token":str(refresh.access_token),
                                    "refresh_token":str(refresh)
                            }, status=status.HTTP_200_OK)
                        else:
                            user.objects.create_realtor(name=name, email=email, password=password)

                            return Response(
                                {'success':'Realtor created successfully'},
                                status=status.HTTP_201_CREATED
                            )
                    else:
                        return Response(
                            {'error':'User with this Email already exists'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {'error':'Password must be at least 8 characters long'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'error':'Passwords do not match'},
                    status=status.HTTP_400_BAD_REQUEST
                ) 
        except:
            return Response(
                {'error':'Something went wrong WHEN registering an  account'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LoginView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        email = request.data.get('email', '').lower()
        password = request.data.get('password', '')

        user_obj = authenticate(request, email=email, password=password)
        if user_obj is not None:
            token, created = Token.objects.get_or_create(user=user_obj)
            return Response({
                'message': 'Login successful',
                'token': token.key,
                'user': {
                    'name': user_obj.name,
                    'email': user_obj.email,
                    'is_realtor': user_obj.is_realtor
                }
            }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'success': 'Logged out successfully'}, status=status.HTTP_200_OK)
    
class UserUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def put(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Profile updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RetrieveUserView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            user = UserSerializer(user)
            return Response(
                {'user': user.data}, status=status.HTTP_200_OK)
        except:
            return Response(
                {'error':'Something went wrong when retrieving the user details'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )