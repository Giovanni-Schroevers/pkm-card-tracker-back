from django.db.models import Q
from rest_framework import status, exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from card_tracker_app.models import Action, Set, Card, CardOwned
from card_tracker_app.permissions import IsAdmin
from card_tracker_app.serializers.action import ActionSerializer
from card_tracker_app.serializers.card import CardSerializer, CardInSetSerializer
from card_tracker_app.serializers.card_owned import CardOwnedSerializer
from card_tracker_app.serializers.set import SetSerializer


@api_view(['GET'])
def set_overview(request):
    sets = SetSerializer(Set.objects.all(), many=True).data

    for pkm_set in sets:
        cards = Card.objects.filter(~Q(rarity='Rare Secret'), card_card_owned__is_loan=False,
                                    set=pkm_set['id']).distinct()
        cards_sr = Card.objects.filter(card_card_owned__is_loan=False,
                                    set=pkm_set['id']).distinct()
        pkm_set['owned_cards'] = len(cards)
        pkm_set['owned_cards_sr'] = len(cards_sr)

    return Response(sets, status=status.HTTP_200_OK)


@api_view(['GET'])
def set_detail(request, pk):
    try:
        pkm_set = Set.objects.get(pk=pk)
    except Set.DoesNotExist:
        raise exceptions.NotFound(f"Set with name '{pk}' does not exist")

    cards = CardInSetSerializer(Card.objects.filter(set=pkm_set.id), many=True).data

    for card in cards:
        card['total_cards'] = len(CardOwned.objects.filter(card=card['id'], is_loan=False))

    data = SetSerializer(pkm_set).data
    data['cards'] = cards

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def set_detail_by_name(request, name):
    try:
        pkm_set = Set.objects.get(name__iexact=name)
    except Set.DoesNotExist:
        raise exceptions.NotFound(f"Set with name '{name}' does not exist")

    cards = CardInSetSerializer(Card.objects.filter(set=pkm_set.id), many=True).data

    for card in cards:
        card['total_cards'] = len(CardOwned.objects.filter(card=card['id'], is_loan=False))

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
@permission_classes((IsAdmin,))
def upsert(request):
    if not request.data:
        raise exceptions.ParseError('Missing body')

    data = request.data

    pkm_set = Set.objects.get(name=data['name'])

    if pkm_set:
        set_validate = SetSerializer(pkm_set, data, partial=True)
    else:
        set_validate = SetSerializer(data=data)

    set_validate.is_valid(raise_exception=True)
    pkm_set = set_validate.save()

    for card in data['cards']:
        card_db = Card.objects.get(set=pkm_set.id, number=card['number'])
        card['set'] = pkm_set.id
        if card_db:
            card_validate = CardSerializer(card_db, card, partial=True)
        else:
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

    action_data = {'user': user.id, 'card': card.id}

    if action_type == 'add':
        card_owned = CardOwnedSerializer(data=action_data)
        card_owned.is_valid()
        card_owned.save()

        action_data['action'] = 0
    elif action_type == 'loan':
        total_cards = CardOwned.objects.filter(card=card.id, is_loan=False)
        loaned_cards = CardOwned.objects.filter(card=card.id, is_loan=True)

        if len(total_cards) > len(loaned_cards):
            action_data['action'] = 1

            card_owned = CardOwnedSerializer(data={'user': user.id, 'card': card.id, 'is_loan': True})
            card_owned.is_valid()
            card_owned.save()
        else:
            return Response({'detail': 'There are no cards to be loaned'}, status=status.HTTP_400_BAD_REQUEST)
    elif action_type == 'return':
        loans = CardOwned.objects.filter(user=request.user.id, card=card.id, is_loan=True)

        if len(loans) == 0:
            return Response({'detail': 'You can not return cards that were not loaned by yourself'},
                            status=status.HTTP_400_BAD_REQUEST)

        CardOwned.delete(loans.last())

        action_data['action'] = 2
    elif action_type == 'remove':
        cards = CardOwned.objects.filter(user=request.user.id, card=card.id, is_loan=False)

        if len(cards) == 0:
            cards = CardOwned.objects.filter(card=card.id, is_loan=False)

        if len(cards) > 0:
            CardOwned.delete(cards.last())
        else:
            return Response({'detail': 'You can not remove cards that were not added by yourself / are not in the '
                                       'collection'}, status=status.HTTP_400_BAD_REQUEST)
        action_data['action'] = 3
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

    owned_cards = CardOwned.objects.filter(card=card.id, is_loan=False)
    loaned_cards = CardOwned.objects.filter(card=card.id, is_loan=True)

    additions = []
    loans = []

    for add_action in owned_cards:
        index = next((index for (index, d) in enumerate(additions) if d['name'] == add_action.user.name), None)
        if not type(index) is int:
            additions.append({'name': add_action.user.name, 'amount': 1})
        else:
            additions[index]['amount'] += 1

    for loan_action in loaned_cards:
        index = next((index for (index, d) in enumerate(loans) if d['name'] == loan_action.user.name), None)
        if not type(index) is int:
            loans.append({'name': loan_action.user.name, 'amount': 1})
        else:
            loans[index]['amount'] += 1

    actions = Action.objects.filter(card=card.id)
    action_data = []

    for pkm_action in actions:
        action_data.append(
            {'name': pkm_action.user.name, 'action': pkm_action.action.name, 'timestamp': pkm_action.created_at}
        )

    data['actions'] = action_data
    data['set'] = Set.objects.get(pk=data['set']).name
    data['additions'] = additions
    data['loans'] = loans

    return Response(data, status=status.HTTP_200_OK)
