from django.urls import path

from .views.user import create as create_user
from .views.set import upsert as upsert_set
from .views import *

urlpatterns = [
    path('login/', login),
    path('reset-password/', reset_password),
    path('user/create/', create_user),
    path('user/<int:pk>/update/', update),
    path('user/change-password/', change_password),
    path('set/', set_overview),
    path('set/upsert/', upsert_set),
    path('set/<int:pk>/', set_detail),
    path('set/<int:pk>/cards_per_row/', set_cards_per_row),
    path('set/<str:name>/', set_detail_by_name),
    path('set/<int:set_id>/<str:card_id>/', action),
    path('card/<int:pk>/', card_detail),
    path('card/<int:pk>/comment/', comment)
]
