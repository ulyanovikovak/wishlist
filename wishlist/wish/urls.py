from django.urls import path

from .views import GiftCreateView, GiftDetailView, GiftListView

urlpatterns = [
    path("create/", GiftCreateView.as_view(), name="gift-create"),
    path("", GiftListView.as_view(), name="gift-list"),
    path("<int:pk>/", GiftDetailView.as_view(), name="gift-detail"),
]
