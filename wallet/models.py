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
    contractRet = models.CharField(max_length=50)
    fee = models.IntegerField()
    signature = models.CharField(max_length=255)
    txID = models.CharField(max_length=128, primary_key=True)
    net_usage = models.IntegerField()
    raw_data_hex = models.CharField(max_length=512)
    net_fee = models.IntegerField()
    energy_usage = models.IntegerField()
    blockNumber = models.IntegerField()
    block_timestamp = models.CharField(max_length=50)
    energy_fee = models.IntegerField()
    energy_usage_total = models.IntegerField()
    # amount = models.BigIntegerField()
    owner_address = models.CharField(max_length=128)
    # to_address = models.CharField(max_length=128)
    type_url = models.CharField(max_length=255)
    _type = models.CharField(max_length=128)
    ref_block_bytes = models.CharField(max_length=50)
    ref_block_hash = models.CharField(max_length=64)
    expiration = models.BigIntegerField()
    timestamp = models.BigIntegerField()


    
class TransferData(models.Model):
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
    