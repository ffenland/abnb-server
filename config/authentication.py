from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User


class TrustMeAuth(BaseAuthentication):
    def authenticate(self, request):
        ## return user or None
        username = request.headers.get("Trust-Me")
        if not username:
            return None
        else:
            try:
                user = User.objects.get(username=username)
                return (user, None)
            except User.DoesNotExist:
                raise AuthenticationFailed("No username")
