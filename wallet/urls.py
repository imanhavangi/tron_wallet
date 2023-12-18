# wallet/urls.py
from django.urls import path
from .views import CreateWallet
from .views import WalletBalance
from .views import AllContractBalance
from .views import AllTransactions

urlpatterns = [
    path('wallet/', CreateWallet.as_view(), name='create-wallet'),
    path('getbalance/', WalletBalance.as_view(), name='get-balance'),
    path('getAllContractBalance/', AllContractBalance.as_view(), name='get-all-contract-balance'),
    path('getAllTransactions/', AllTransactions.as_view(), name='get-all-transactions')
]
