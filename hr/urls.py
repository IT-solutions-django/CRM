from django.urls import path
from .views import *


app_name = 'hr'


urlpatterns = [
    path('', HRView.as_view(), name='hr'),
]