from rest_framework import status, exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from card_tracker_app.models import User, Set, Card, Action
from card_tracker_app.permissions import IsAdmin
from card_tracker_app.serializers.action import ActionSerializer
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


@api_view(['PUT'])
def action(request, set_id, card_number):
    if not request.data:
        raise exceptions.ParseError('Missing body')

    try:
        pkm_set = Set.objects.get(id=set_id)
    except Set.DoesNotExist:
        raise exceptions.NotFound(f"Set with id '{set_id}' does not exist")

    try:
        card = Card.objects.get(set=set_id, number=card_number)
    except Card.DoesNotExist:
        raise exceptions.NotFound(f"Card '{card_number}' does not exist in set '{pkm_set.name}'")

    if 'action' not in request.data:
        raise exceptions.ParseError('Missing parameter action')

    user = request.user
    action_type = request.data['action']

    action_data = {'user': user.id, 'set': pkm_set.id, 'card': card.id}

    if action_type == 'add':
        action_data['action'] = 0
    elif action_type == 'loan':
        total_cards = Action.objects.filter(card=card.id, action=0)
        loaned_cards = Action.objects.filter(card=card.id, action=1)

        if len(total_cards) > len(loaned_cards):
            action_data['action'] = 1
        else:
            return Response({'detail': 'There are no cards to be loaned'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        raise exceptions.ParseError(f"{action_type} is not a valid action")

    action_validate = ActionSerializer(data=action_data)
    action_validate.is_valid(raise_exception=True)
    action_validate.save()

    return Response(status=status.HTTP_204_NO_CONTENT)
