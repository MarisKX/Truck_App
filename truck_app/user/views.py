"""
Views for the user API
"""
from django.http import JsonResponse
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView


from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        response_data = {
            'user_id': user.pk,
            'username': user.email,
            'token': token.key,
        }

        response = JsonResponse(response_data)
        print("Setting cookie...")
        response.set_cookie('auth_token', token.key, httponly=False, samesite='Lax')
        print("Cookie set!")

        return response


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authentcated user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class CheckAuth(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        print("Received auth header:", auth_header)

        if "Token" in auth_header:
            # Extract the token key from the Authorization header
            token_key = auth_header.split(" ")[1]

            try:
                # Retrieve the token object based on the key
                token = Token.objects.get(key=token_key)

                # Print the token's created timestamp
                print("Token created at:", token.created)

            except Token.DoesNotExist:
                print("Invalid token")

        return Response({"authenticated": True})
