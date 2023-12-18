# wallet/urls.py
from django.urls import path
from .views import CreateWallet
from .views import WalletBalance

urlpatterns = [
    path('wallet/', CreateWallet.as_view(), name='create-wallet'),
    path('getbalance/', WalletBalance.as_view(), name='get-balance'),
]
