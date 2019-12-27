from rest_framework import status, exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from card_tracker_app.models import Action, Set, Card
from card_tracker_app.permissions import IsAdmin
from card_tracker_app.serializers.action import ActionSerializer
from card_tracker_app.serializers.card import CardSerializer, CardInSetSerializer
from card_tracker_app.serializers.set import SetSerializer


@api_view(['GET'])
def set_overview(request):
    sets = SetSerializer(Set.objects.all(), many=True).data

    for pkm_set in sets:
        cards = Card.objects.filter(card_action__action=0).distinct()
        pkm_set['owned_cards'] = len(cards)

    return Response(sets, status=status.HTTP_200_OK)


@api_view(['GET'])
def set_detail(request, pk):
    try:
        pkm_set = Set.objects.get(pk=pk)
    except Set.DoesNotExist:
        raise exceptions.NotFound(f"Set with id '{pk}' does not exist")

    cards = CardInSetSerializer(Card.objects.filter(set=pkm_set.id), many=True).data

    for card in cards:
        card['total_cards'] = len(Action.objects.filter(card=card['id'], action=0))

    data = SetSerializer(pkm_set).data
    data['cards'] = cards

    return Response(data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes((IsAdmin,))
def create(request):
    if not request.data:
        raise exceptions.ParseError('Missing body')

    data = request.data

    set_validate = SetSerializer(data=data)
    set_validate.is_valid(raise_exception=True)
    pkm_set = set_validate.save()

    for card in data['cards']:
        card['set'] = pkm_set.id
        card_validate = CardSerializer(data=card)
        card_validate.is_valid(raise_exception=True)
        card_validate.save()

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
    elif action_type == 'remove':
        actions = Action.objects.filter(action=0, user=request.user.id, card=card.id).order_by('created_at')

        if len(actions) == 0:
            actions = Action.objects.filter(action=0, card=card.id).order_by('created_at')

        if len(actions) > 0:
            Action.delete(actions.last())
        else:
            return Response({'detail': 'You can not remove cards that were not added by yourself / are not in the '
                                       'collection'}, status=status.HTTP_400_BAD_REQUEST)
        action_data['action'] = 2
    else:
        raise exceptions.ParseError(f"{action_type} is not a valid action")

    action_validate = ActionSerializer(data=action_data)
    action_validate.is_valid(raise_exception=True)
    action_validate.save()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def card_detail(request, pk):
    try:
        card = Card.objects.get(pk=pk)
    except Card.DoesNotExist:
        raise exceptions.NotFound(f"Card with id'{pk}' not found")

    data = CardSerializer(card).data

    actions = Action.objects.filter(card=card.id)
    action_data = []

    for pkm_action in actions:
        action_data.append(
            {'name': pkm_action.user.name, 'action': pkm_action.action.name, 'timestamp': pkm_action.created_at}
        )

    data['actions'] = action_data
    data['set'] = Set.objects.get(pk=data['set']).name

    return Response(data, status=status.HTTP_200_OK)

