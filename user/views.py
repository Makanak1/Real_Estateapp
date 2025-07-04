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
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
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
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        
        email = request.data.get('email', '').lower()
        password = request.data.get('password', '')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)

            return Response({
                "message": f"{user.name} logged in successfully",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "is_realtor": user.is_realtor
            }, status=status.HTTP_200_OK)

        return Response({
            "error": "Invalid credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)
        
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"success": "Logged out successfully"}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
    
class UserUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def put(self, request):
        user = request.user
        data = request.data.copy()

        # Extract password if provided
        password = data.pop('password', None)

        serializer = UserUpdateSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Set and save new password securely
            if password:
                user.set_password(password)
                user.save()

            return Response({'success': 'Profile updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RetrieveUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
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