from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from card_tracker_app.permissions import IsAdmin
from card_tracker_app.serializers.user import UserSerializer, PasswordSerializer


@api_view(['PUT'])
@permission_classes((IsAdmin,))
def create(request):
    if not request.data:
        return Response({'detail': 'Missing body'}, status=status.HTTP_400_BAD_REQUEST)

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
        return Response({'detail': 'Missing body'}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data
    user = request.user

    password = PasswordSerializer(data=data)
    password.is_valid(raise_exception=True)

    user.set_password(password.data['password'])
    user.save()

    return Response(status=status.HTTP_204_NO_CONTENT)
