from django.urls import path

from .views.user import create as create_user
from .views.set import create as create_set
from .views import *

urlpatterns = [
    path('login/', login),
    path('reset-password/', reset_password),
    path('user/create/', create_user),
    path('user/<int:pk>/update/', update),
    path('user/change-password/', change_password),
    path('set/', set_overview),
    path('set/create/', create_set),
    path('set/<int:pk>/', set_detail),
    path('set/<str:name>/', set_detail_by_name),
    path('set/<int:set_id>/<int:card_number>/', action),
    path('card/<int:pk>/', card_detail)
]
