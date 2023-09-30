"""
Middleware to handle auth token expiry
"""
from django.utils import timezone
from django.http import JsonResponse
from rest_framework.authtoken.models import Token


class TokenExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check for the token in the cookie
        if request.path.startswith('/admin') or request.path.startswith('/api/docs') or request.path.startswith('/api/schema'):
            print("request starts with admin or api")
            # If it's an admin or API path, skip middleware processing
            response = self.get_response(request)
        else:
            print("request starts with Vue urls")
            token_key = request.COOKIES.get('auth_token')
            response = None  # Define response variable here

            if token_key:
                try:
                    token_obj = Token.objects.get(key=token_key)
                except Token.DoesNotExist:
                    response = JsonResponse({"error": "Invalid Token"}, status=401)
                else:
                    last_activity = token_obj.created
                    now = timezone.now()  # Use Django's timezone-aware datetime

                    if (now - last_activity).total_seconds() > 600:  # 15 minutes
                        token_obj.delete()
                        response = JsonResponse({"error": "Token expired"}, status=401)

                if response:
                    response.set_cookie(
                        'auth_token',
                        '',
                        expires='Thu, 01 Jan 1970 00:00:01 GMT',  # This is in the past
                        domain='.maris.com',  # Add this line to allow subdomain access
                        httponly=True,
                        samesite='Lax',
                    )
                else:
                    token_obj.created = now
                    print(token_obj.created)
                    token_obj.save()

                    # Add the token to the request headers
                    request.META['HTTP_AUTHORIZATION'] = f'Token {token_key}'

            if response is None:
                response = self.get_response(request)  # Only get_response if no error occurred

        return response
