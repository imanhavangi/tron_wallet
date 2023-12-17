# wallet/urls.py
from django.urls import path
from .views import WalletListCreateView
from .views import WalletBalance

urlpatterns = [
    path('wallet/', WalletListCreateView.as_view(), name='create-wallet'),
    path('getbalance/', WalletBalance.as_view(), name='get-balance'),
]
