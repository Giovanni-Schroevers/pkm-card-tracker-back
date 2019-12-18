from rest_framework import status, exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from card_tracker_app.models import User
from card_tracker_app.serializers.authentication import LoginSerializer


@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    """Return a User

    Checks the posted email and password
    If it's a match, a token is created and the matched User is returned
    """
    if not request.data:
        return Response({'detail': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)
    data = request.data
    login_validate = LoginSerializer(data=data)
    login_validate.is_valid(raise_exception=True)

    try:
        user = User.objects.get(name=data['name'])
    except User.DoesNotExist:
        raise exceptions.AuthenticationFailed("Wrong login credentials")

    user.set_password("kaas")

    if not user.check_password(data['password']):
        raise exceptions.AuthenticationFailed('Wrong login credentials')

    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key}, status=status.HTTP_200_OK)
