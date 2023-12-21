# wallet/urls.py
from django.urls import path
from .views import CreateWallet
from .views import WalletBalance
from .views import AllContractBalance
from .views import AllTransactions
from .views import AllContractTransfers
from .views import CreateTransaction
from .views import TransactionInfo
from .views import CalculateFee
from .views import SignTransaction

urlpatterns = [
    path('wallet/', CreateWallet.as_view(), name='create-wallet'),
    path('getbalance/', WalletBalance.as_view(), name='get-balance'),
    path('getAllContractBalance/', AllContractBalance.as_view(), name='get-all-contract-balance'),
    path('getAllTransactions/', AllTransactions.as_view(), name='get-all-transactions'),
    path('getAllContractTransfers/', AllContractTransfers.as_view(), name='get-all-contract-transfers'),
    path('createTransaction/', CreateTransaction.as_view(), name='create-transaction'),
    path('transactionInfo/', TransactionInfo.as_view(), name='transaction-info'),
    path('calculateFee/', CalculateFee.as_view(), name='calculate-fee'),
    path('signTransaction/', SignTransaction.as_view(), name='sign-transaction'),
]