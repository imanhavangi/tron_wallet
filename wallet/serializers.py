from rest_framework import serializers
from .models import Trc20Data
from .models import TransactionData

class Trc20DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trc20Data
        fields = ['contract_address', 'count']

class TransactionDataSerializer(serializers.ModelSerializer):
    class Meta:
      model = TransactionData
      fields = '__all__'
    #   fileds = ['transaction_id', 'token_symbol', 'token_address', 'token_decimals', 'token_name', 'block_timestamp', 'from_address', 'to_address', 'transaction_type', 'value']