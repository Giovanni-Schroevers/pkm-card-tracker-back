from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed


# DEFAULT_AUTHENTICATION_CLASSES
class ExpiringTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        """Return user, token

        Checks if the token is: invalid, not active or expired
        gives the token and user of the token
        """
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid Token')

        if not token.user.is_active:
            raise AuthenticationFailed('User is not active')

        return token.user, token
