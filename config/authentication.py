import jwt
from django.conf import settings
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


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_key = request.headers.get("Authorization")
        if not auth_key:
            return None
        auth = auth_key.split()
        if not auth or auth[0].lower() != "bearer":
            return None

        if len(auth) == 1:
            msg = _("Invalid token header. No credentials provided.")
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _("Invalid token header. Token string should not contain spaces.")
            raise AuthenticationFailed(msg)

        try:
            token = auth[1]
            if not token:
                return None
            decoded = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms="HS256",
            )
            pk = decoded.get("pk")
            if not pk:
                raise AuthenticationFailed("Invalid Token")
            try:
                user = User.objects.get(pk=pk)
                return (user, None)
            except User.DoesNotExist:
                raise AuthenticationFailed("User Not Found")
        except UnicodeError:
            msg = _(
                "Invalid token header. Token string should not contain invalid characters."
            )
            raise AuthenticationFailed(msg)
        print(request.headers)
        return None
