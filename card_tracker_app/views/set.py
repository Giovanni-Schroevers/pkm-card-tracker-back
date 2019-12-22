from rest_framework import status, exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from card_tracker_app.models import Series
from card_tracker_app.permissions import IsAdmin
from card_tracker_app.serializers.card import CardSerializer
from card_tracker_app.serializers.set import SetSerializer


@api_view(['PUT'])
@permission_classes((IsAdmin,))
def create(request):
    if not request.data:
        raise exceptions.ParseError('Missing body')

    data = request.data

    if 'series' not in data:
        raise exceptions.ParseError('Missing property series')

    series = Series.objects.get_or_create(name=data['series'])
    data['series'] = series[0].id

    set_validate = SetSerializer(data=data)
    set_validate.is_valid(raise_exception=True)
    pkm_set = set_validate.save()

    for card in data['cards']:
        card['set'] = pkm_set.id
        card_validate = CardSerializer(data=card)
        card_validate.is_valid(raise_exception=True)
        card_validate.save()

    return Response(status=status.HTTP_204_NO_CONTENT)
