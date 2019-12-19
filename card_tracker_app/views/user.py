from rest_framework import status, exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from card_tracker_app.models import User
from card_tracker_app.permissions import IsAdmin
from card_tracker_app.serializers.user import UserSerializer, PasswordSerializer


@api_view(['PUT'])
@permission_classes((IsAdmin,))
def create(request):
    if not request.data:
        raise exceptions.ParseError('Missing body')

    data = request.data
    user_validate = UserSerializer(data=data)
    user_validate.is_valid(raise_exception=True)
    user = user_validate.save()
    password = data['password']
    user.set_password(password)
    user.save()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
def change_password(request):
    if not request.data:
        raise exceptions.ParseError('Missing body')

    data = request.data
    user = request.user

    password = PasswordSerializer(data=data)
    password.is_valid(raise_exception=True)

    user.set_password(password.data['password'])
    user.save()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
@permission_classes((IsAdmin,))
def update(request, pk):
    if not request.data:
        raise exceptions.ParseError('Missing body')

    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        raise exceptions.NotFound(f"User with id '{pk}' does not exist")

    data = request.data

    user_validate = UserSerializer(user, data=data, partial=True)
    user_validate.is_valid(raise_exception=True)

    user_validate.update(instance=user, validated_data=user_validate.data)

    return Response(status=status.HTTP_204_NO_CONTENT)




