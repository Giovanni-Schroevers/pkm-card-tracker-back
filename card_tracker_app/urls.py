from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login),
    path('reset-password/', reset_password),
    path('user/create/', create),
    path('user/<int:pk>/update/', update),
    path('user/change-password/', change_password),
]
