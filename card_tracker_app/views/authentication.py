from smtplib import SMTPException

from django.core.mail import send_mail, BadHeaderError
from django.utils.crypto import get_random_string
from rest_framework import status, exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from card_tracker_app.models import User
from card_tracker_app.serializers.authentication import LoginSerializer, ResetPasswordSerializer


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

    if not user.check_password(data['password']):
        raise exceptions.AuthenticationFailed('Wrong login credentials')

    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def reset_password(request):
    """Return information and send an email

    Checks the posted email
    If the user exists, their password is reset and an email with the new password is sent
    """
    if not request.data:
        return Response({'detail': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    data = request.data
    password_reset = ResetPasswordSerializer(data=data)
    password_reset.is_valid(raise_exception=True)
    email = data['email']

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise exceptions.NotFound(f"User with email '{email}' does not exist")

    password = get_random_string()

    try:
        send_mail(
            subject='Password reset',
            message=f'Your newly generated password is: {password}',
            from_email='no-reply@shinebrothers.nl',
            recipient_list=[email],
        )
    except BadHeaderError:
        return Response({'detail': 'Invalid header found'}, status=status.HTTP_400_BAD_REQUEST)
    except SMTPException:
        return Response({'detail': 'There was an error sending the email'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    user.set_password(password)
    user.save()

    return Response({'detail': 'A new password has been sent to your mailbox at: ' + email},
                    status=status.HTTP_200_OK)
