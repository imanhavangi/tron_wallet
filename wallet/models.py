# tron_wallet/models.py
from django.db import models

class TronAccount(models.Model):
    address = models.CharField(max_length=50)
    balance = models.BigIntegerField()
    create_time = models.BigIntegerField()
    net_window_size = models.BigIntegerField()
    net_window_optimized = models.BooleanField()
    # Add other fields as needed
    
class Trc20Data(models.Model):
    contract_address = models.CharField(max_length=255)
    count = models.CharField(max_length=255)
    
class TransactionData(models.Model):
    transaction_id = models.CharField(max_length=128, primary_key=True)
    token_symbol = models.CharField(max_length=255)
    token_address = models.CharField(max_length=255)
    token_decimals = models.IntegerField()
    token_name = models.CharField(max_length=255)
    block_timestamp = models.CharField(max_length=255)
    from_address = models.CharField(max_length=255)
    to_address = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    