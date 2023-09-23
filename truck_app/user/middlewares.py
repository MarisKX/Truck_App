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
        # Code to be executed for each request before the view is called
        token = request.META.get("HTTP_AUTHORIZATION")

        if token:
            print(token)
            try:
                token_obj = Token.objects.get(key=token.split(" ")[1])
            except Token.DoesNotExist:
                return JsonResponse({"error": "Invalid Token"}, status=401)

            last_activity = token_obj.created
            now = timezone.now()  # Use Django's timezone-aware datetime

            if (now - last_activity).total_seconds() > 900:  # 15 minutes
                token_obj.delete()
                return JsonResponse({"error": "Token expired"}, status=401)

            token_obj.created = now
            token_obj.save()

        response = self.get_response(request)

        return response
