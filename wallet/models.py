# tron_wallet/models.py
from django.db import models

class TronAccount(models.Model):
    address = models.CharField(max_length=50)
    balance = models.BigIntegerField()
    create_time = models.BigIntegerField()
    net_window_size = models.BigIntegerField()
    net_window_optimized = models.BooleanField()
    # Add other fields as needed