from django.urls import path

from .views import GiftCreateView

urlpatterns = [
    path('create/', GiftCreateView.as_view(), name='gift-create'),
]